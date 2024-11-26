# Use Node.js LTS version as the base image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
RUN npm install
RUN npm install mysql2

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["node", "index.js"]
