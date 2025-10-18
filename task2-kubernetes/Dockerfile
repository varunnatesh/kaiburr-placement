# Use Maven image to build
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy backend pom and download dependencies
COPY task1-java-backend/pom.xml ./pom.xml
RUN mvn -q dependency:go-offline

# Copy backend source code and build
ARG CACHEBUST=1
COPY task1-java-backend/src ./src
RUN mvn -q clean package -DskipTests

# Use JRE image for runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Copy JAR from build stage
COPY --from=build /app/target/task-manager-1.0.0.jar app.jar

# Expose port
EXPOSE 8080

# Run application
ENTRYPOINT ["java", "-jar", "app.jar"]
