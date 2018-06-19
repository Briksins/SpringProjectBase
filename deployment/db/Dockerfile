FROM postgres:10.4-alpine

########## Add Health Check ##########
HEALTHCHECK --interval=30s --timeout=15s CMD pg_isready -U postgres  || exit 1
