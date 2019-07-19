# Generated for android-64 and Python v3.7.2.

TEMPLATE = app

CONFIG += warn_off

QMAKE_CFLAGS += -std=c99

RESOURCES = \
    resources/pyqtdeploy.qrc

DEFINES += PYQTDEPLOY_FROZEN_MAIN PYQTDEPLOY_OPTIMIZED

INCLUDEPATH += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules
INCLUDEPATH += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_blake2
INCLUDEPATH += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_sha3
INCLUDEPATH += /home/sunyudong/git/photonLauncher/micron/project_guimicro/sysroot-android-64/include
INCLUDEPATH += /home/sunyudong/git/photonLauncher/micron/project_guimicro/sysroot-android-64/include/python3.7

SOURCES = pyqtdeploy_main.cpp pyqtdeploy_start.cpp pdytools_module.cpp
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_abc.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_bisectmodule.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_blake2/blake2b_impl.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_blake2/blake2module.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_blake2/blake2s_impl.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_bz2module.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_datetimemodule.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_heapqmodule.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_math.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_posixsubprocess.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_randommodule.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_sha3/sha3module.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/_struct.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/binascii.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/cjkcodecs/_codecs_cn.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/cjkcodecs/_codecs_hk.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/cjkcodecs/_codecs_iso2022.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/cjkcodecs/_codecs_jp.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/cjkcodecs/_codecs_kr.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/cjkcodecs/_codecs_tw.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/cjkcodecs/multibytecodec.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/mathmodule.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/md5module.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/selectmodule.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/sha1module.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/sha256module.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/sha512module.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/socketmodule.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/termios.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/unicodedata.c
SOURCES += /home/sunyudong/git/photonLauncher/micron/project_guimicro/Modules/zlibmodule.c

HEADERS = pyqtdeploy_version.h frozen_bootstrap.h frozen_bootstrap_external.h frozen_main.h

LIBS += -L/home/sunyudong/git/photonLauncher/micron/project_guimicro/sysroot-android-64/lib
LIBS += -L/usr/include
LIBS += -L/usr/lib/python3.7/site-packages
LIBS += -L/usr/lib/python3.7/site-packages/PyQt5
LIBS += -lQt
LIBS += -lQtCore
LIBS += -lQtGui
LIBS += -lbz2
LIBS += -lpython3
LIBS += -lsip
LIBS += -lz

ANDROID_EXTRA_LIBS += /home/sunyudong/git/photonLauncher/micron/project_guimicro/sysroot-android-64/lib/libbz2.so /home/sunyudong/git/photonLauncher/micron/project_guimicro/sysroot-android-64/lib/libz.so

cython.name = Cython compiler
cython.input = CYTHONSOURCES
cython.output = ${QMAKE_FILE_BASE}.c
cython.variable_out = GENERATED_SOURCES
cython.commands = cython ${QMAKE_FILE_IN} -o ${QMAKE_FILE_OUT}

QMAKE_EXTRA_COMPILERS += cython

linux-* {
    LIBS += -lutil -ldl
}

win32 {
    masm.input = MASMSOURCES
    masm.output = ${QMAKE_FILE_BASE}.obj

    contains(QMAKE_TARGET.arch, x86_64) {
        masm.name = MASM64 compiler
        masm.commands = ml64 /Fo ${QMAKE_FILE_OUT} /c ${QMAKE_FILE_IN}
    } else {
        masm.name = MASM compiler
        masm.commands = ml /Fo ${QMAKE_FILE_OUT} /c ${QMAKE_FILE_IN}
    }

    QMAKE_EXTRA_COMPILERS += masm

    LIBS += -lshlwapi -ladvapi32 -lshell32 -luser32 -lws2_32 -lole32 -loleaut32 -lversion
    DEFINES += MS_WINDOWS _WIN32_WINNT=Py_WINVER NTDDI_VERSION=Py_NTDDI WINVER=Py_WINVER

    # This is added from the qmake spec files but clashes with _pickle.c.
    DEFINES -= UNICODE
}

macx {
    LIBS += -framework SystemConfiguration -framework CoreFoundation
}
