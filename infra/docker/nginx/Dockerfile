# Custom Nginx image to add our specific configuration
FROM nginx:alpine

# Remove default nginx configs
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom config (created earlier)
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]