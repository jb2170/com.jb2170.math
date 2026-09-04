SRC=hugo
BUILD=${SRC}/public
PUBLIC_HTML=jb2170@SAO:~/http/com.jb2170.math/public/

.PHONY: all
all:

.PHONY: build
build:
	hugo --source ${SRC} build

.PHONY: wait
wait:
	hugo --source ${SRC} build -w

.PHONY: sync
sync:
	rsync    -vzaHc --no-t --del --chmod o=rX \
	${BUILD}/ \
	${PUBLIC_HTML}

.PHONY: syncn
syncn:
	rsync -n -vzaHc --no-t --del --chmod o=rX \
	${BUILD}/ \
	${PUBLIC_HTML}

.PHONY: clean
clean:
	rm -rf ${BUILD}
