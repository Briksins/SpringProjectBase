FROM openjdk:8u151-jre-alpine3.7

########## Add Health Check ##########
RUN apk add --no-cache curl
HEALTHCHECK --interval=30s --timeout=15s CMD curl -f http://localhost:8080/api/health || exit 1

########## Add User and Group ##########
ENV SPRING_GROUP spring-group
ENV SPRING_GRPOUP_ID 1001
ENV SPRING_USER spring
ENV SPRING_USER_ID 1001
ENV SPRING_HOME /var/www/spring

RUN mkdir -p ${SPRING_HOME}
RUN addgroup -g ${SPRING_GRPOUP_ID} ${SPRING_GROUP}
RUN adduser -S -s /bin/false -h ${SPRING_HOME} -u ${SPRING_USER_ID} ${SPRING_USER} ${SPRING_GROUP}

##########  Deploy Spring Boot Jar File ##########
COPY build/libs/*.jar ${SPRING_HOME}/
RUN chown -R ${SPRING_USER}:${SPRING_GROUP} ${SPRING_HOME}

##########  Container Execution ##########
EXPOSE 8080
USER ${SPRING_USER}
CMD java -jar ${SPRING_HOME}/*jar
