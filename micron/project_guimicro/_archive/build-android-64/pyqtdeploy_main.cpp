#include <Python.h>
#include <QtGlobal>


extern "C" PyObject *PyInit_Qt(void);
extern "C" PyObject *PyInit_QtCore(void);
extern "C" PyObject *PyInit_QtGui(void);
extern "C" PyObject *PyInit__abc(void);
extern "C" PyObject *PyInit__bisect(void);
extern "C" PyObject *PyInit__blake2(void);
extern "C" PyObject *PyInit__bz2(void);
extern "C" PyObject *PyInit__codecs_cn(void);
extern "C" PyObject *PyInit__codecs_hk(void);
extern "C" PyObject *PyInit__codecs_iso2022(void);
extern "C" PyObject *PyInit__codecs_jp(void);
extern "C" PyObject *PyInit__codecs_kr(void);
extern "C" PyObject *PyInit__codecs_tw(void);
extern "C" PyObject *PyInit__datetime(void);
extern "C" PyObject *PyInit__heapq(void);
extern "C" PyObject *PyInit__md5(void);
extern "C" PyObject *PyInit__multibytecodec(void);
extern "C" PyObject *PyInit__posixsubprocess(void);
extern "C" PyObject *PyInit__random(void);
extern "C" PyObject *PyInit__sha1(void);
extern "C" PyObject *PyInit__sha256(void);
extern "C" PyObject *PyInit__sha3(void);
extern "C" PyObject *PyInit__sha512(void);
extern "C" PyObject *PyInit__socket(void);
extern "C" PyObject *PyInit__struct(void);
extern "C" PyObject *PyInit_binascii(void);
extern "C" PyObject *PyInit_math(void);
extern "C" PyObject *PyInit_select(void);
extern "C" PyObject *PyInit_sip(void);
extern "C" PyObject *PyInit_termios(void);
extern "C" PyObject *PyInit_unicodedata(void);
extern "C" PyObject *PyInit_zlib(void);

static struct _inittab extension_modules[] = {
    {"PyQt5.Qt", PyInit_Qt},
    {"PyQt5.QtCore", PyInit_QtCore},
    {"PyQt5.QtGui", PyInit_QtGui},
    {"_abc", PyInit__abc},
    {"_bisect", PyInit__bisect},
    {"_blake2", PyInit__blake2},
    {"_bz2", PyInit__bz2},
    {"_codecs_cn", PyInit__codecs_cn},
    {"_codecs_hk", PyInit__codecs_hk},
    {"_codecs_iso2022", PyInit__codecs_iso2022},
    {"_codecs_jp", PyInit__codecs_jp},
    {"_codecs_kr", PyInit__codecs_kr},
    {"_codecs_tw", PyInit__codecs_tw},
    {"_datetime", PyInit__datetime},
    {"_heapq", PyInit__heapq},
    {"_md5", PyInit__md5},
    {"_multibytecodec", PyInit__multibytecodec},
    {"_posixsubprocess", PyInit__posixsubprocess},
    {"_random", PyInit__random},
    {"_sha1", PyInit__sha1},
    {"_sha256", PyInit__sha256},
    {"_sha3", PyInit__sha3},
    {"_sha512", PyInit__sha512},
    {"_socket", PyInit__socket},
    {"_struct", PyInit__struct},
    {"binascii", PyInit_binascii},
    {"math", PyInit_math},
    {"select", PyInit_select},
    {"sip", PyInit_sip},
    {"termios", PyInit_termios},
    {"unicodedata", PyInit_unicodedata},
    {"zlib", PyInit_zlib},
    {NULL, NULL}
};
static const char *path_dirs[] = {
    "/mnt/YSunDisk/sysroot/",
    NULL
};



extern int pyqtdeploy_start(int argc, char **argv,
        struct _inittab *extension_modules, const char *main_module,
        const char *entry_point, const char **path_dirs);

int main(int argc, char **argv)
{
    return pyqtdeploy_start(argc, argv, extension_modules, "__main__", NULL, path_dirs);
}
