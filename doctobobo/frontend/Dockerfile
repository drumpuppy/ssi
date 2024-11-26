# Step 1: Use a Node.js image to build the app
FROM node:16 as build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the app for production
RUN npm run build

# Step 2: Use an Nginx image to serve the app
FROM nginx:alpine

# Copy the build output to the Nginx HTML directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose the default Nginx port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
