FROM openjdk:8
COPY marple-1.0.jar /
WORKDIR /
# RUN javac Main.java
ENTRYPOINT ["java", "-Ddw.indexPath=/central-lucene-index", "-jar", "/marple-1.0.jar", "server"]