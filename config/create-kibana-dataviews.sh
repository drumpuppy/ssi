#!/bin/bash

# Get Kibana Admin Password from Kubernetes Secret
KIBANA_PASSWORD=$(kubectl get secret elasticsearch-master-credentials -n default -o jsonpath="{.data.password}" | base64 -d)
echo "Using Kibana Password: $KIBANA_PASSWORD"

# Kibana API Credentials
kubectl port-forward svc/kibana-kibana -n default 5601:5601 &
KIBANA_URL="http://localhost:5601"
KIBANA_USER="elastic"

create_data_view() {
  local data_view_id=$1
  local index_pattern=$2
  local search_filter=$3

  RESPONSE=$(curl -s -o response.txt -w "%{http_code}" -X POST "$KIBANA_URL/api/data_views/data_view" \
    -u "$KIBANA_USER:$KIBANA_PASSWORD" \
    -H "kbn-xsrf: true" \
    -H "Content-Type: application/json" \
    -d "{
      \"data_view\": {
        \"title\": \"$index_pattern\",
        \"name\": \"$data_view_id\",
        \"timeFieldName\": \"@timestamp\",
        \"fields\": {
          \"message\": { \"type\": \"text\" },
          \"agent.hostname\": { \"type\": \"keyword\" }
        },
        \"fieldAttrs\": {
          \"message\": { \"customLabel\": \"Log Message\" },
          \"agent.hostname\": { \"customLabel\": \"Host\" }
        },
        \"filter\": {
          \"query\": {
            \"language\": \"kuery\",
            \"query\": \"$search_filter\"
          }
        }
      }
    }")

    if [[ "$RESPONSE" != "200" && "$RESPONSE" != "201" ]]; then
        echo "⚠️ Failed to create Kibana Data View (HTTP $RESPONSE)"
        echo "🔍 Response from Kibana:"
        cat response.txt
        exit 1
    fi

}

# Create Data Views
create_data_view "Istio Logs" "filebeat-generic-*" "istio"
create_data_view "Falco Alerts" "filebeat-generic-*" "falco"
create_data_view "Wazuh Alerts" "filebeat-generic-*" "wazuh"
create_data_view "Generic Logs" "filebeat-generic-*" "*"
