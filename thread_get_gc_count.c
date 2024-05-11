#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
// #include <time.h>

// static PyObject *global_var = NULL;
volatile short terminate_flag = 0;
volatile short terminate_flag_refchain = 0;
FILE *output_fd = NULL;
static int glob_do_IO;

// static void thread_func(void *arg){
//     output_fd = (FILE*)arg;
//     while(!terminate_flag){
//         PyGILState_STATE gstate = PyGILState_Ensure();
//         // struct timespec ts;
//         // clock_gettime(CLOCK_REALTIME, &ts);
//         // fprintf(output_fd, "%ld.%ld\n", ts.tv_sec, ts.tv_nsec);
//         // fflush(output_fd);
//         Py_ssize_t gen = 0;
//         intptr_t ptrint_extended = (intptr_t)gc_get_objects_impl_no_mod(gen);
//         intptr_t ptrint_masked = ptrint_extended & 0x00007FFFFFFFFFFF; // have to do this

//         PyObject * result = (PyObject *)ptrint_masked;
//         Py_ssize_t cur_size = PyList_Size(result);
//         fprintf(output_fd, "Size of list %zd: %zd\n", gen, cur_size);
//         for (Py_ssize_t i = 0; i < cur_size; i++) {
//             PyObject *item = PyList_GetItem(result, i);
//             PyObject *repr = PyObject_Repr(item);
//             if (repr) {
//                 fprintf(output_fd, "%s\n", PyUnicode_AsUTF8(repr));
//                 Py_DECREF(repr);
//             }
//         }
//         Py_BEGIN_ALLOW_THREADS
//             usleep(500000);
//         Py_END_ALLOW_THREADS
//         PyGILState_Release(gstate);
//     }
//     fprintf(stderr, "getout\n");
// }

static void test_thread_funct(void *arg)
{
    PyGILState_STATE gstate = PyGILState_Ensure();
    Py_ssize_t len = 10;
    long long_ = 100;
    double double_ = 100.0;
    // PyObject *test = PyList_New(len); //True
    // PyObject *test = PyDict_New(); // True
    // PyObject *test = PyLong_FromLong(long_); //False
    // PyObject *test = PyTuple_New(len); //True
    // PyObject *test = PyFloat_FromDouble(double_); // False
    const char *str = "123";
    PyObject *test = PyByteArray_FromStringAndSize(str, len); // True

    PyObject *inner_iterator = PyObject_GetIter(test);
    if (inner_iterator)
    {
        fprintf(stderr, "true\n");
    }
    else
    {
        fprintf(stderr, "false\n");
    }
    Py_DECREF(test);
    PyGILState_Release(gstate);
}
// void *peek_gc_list(void *arg)
// {
//     fprintf(stderr, "start peeking thread\n");
//     while (!terminate_flag)
//     {
//         PyGILState_STATE gstate = PyGILState_Ensure();
//         Py_ssize_t generation = -1;
//         PyObject *wrong_result = gc_get_objects_impl_no_mod(generation);

//         /* this is a weird problem that it automatically adds extra higher bits, so I have to truncate */
//         intptr_t wrong_result_casted = (intptr_t)wrong_result;
//         intptr_t correct_result = wrong_result_casted & 0x00007FFFFFFFFFFF;
//         PyObject *result = (PyObject *)correct_result;
//         // fprintf(stderr, "%p\n", result);

//         Py_ssize_t cur_size = PyList_Size(result);
//         fprintf(stderr, "Size is: %zd\n", cur_size);
//         Py_DECREF(result);
//         PyGILState_Release(gstate);
//         usleep(500000);
//     }
//     terminate_flag = 0;
//     Py_RETURN_NONE;
// }

void *sleep_thread_and_close_fd(void *arg)
{
    sleep(1);
    // sleep(179);
    fprintf(stderr, "this should come when closing fd\n");
    if (glob_do_IO)
    {
        fclose(output_fd);
    }
}

static PyObject *start_count_gc_list(PyObject *self, PyObject *args)
{
    PyThreadState *mainThreadState = PyThreadState_Get();
    // fprintf(stderr, "outside: %p\n", mainThreadState);
    unsigned int sample_dur; // sampling duration, for slow scan, in us
    const char *file;        // file name for post processing
    unsigned int doIO;       // do IO or not
    int metadata_resv;
    unsigned int cutoff_limit;
    if (!PyArg_ParseTuple(args, "i|siii", &sample_dur, &file, &doIO, &metadata_resv, &cutoff_limit))
    {
        return NULL; // error
    }
    fprintf(stderr, "file is %s, sample dur is %d\n", file, sample_dur);
    if (doIO)
    {
        glob_do_IO = 1;
        output_fd = fopen(file, "w");
    }
    BookkeepArgs *bookkeepArgs = (BookkeepArgs *)malloc(sizeof(BookkeepArgs));
    bookkeepArgs->sample_dur = sample_dur;
    bookkeepArgs->fd = output_fd;
    // bookkeepArgs->buff_size = buff_size;
    bookkeepArgs->doIO = doIO;
    // bookkeepArgs->gen = gen;
    bookkeepArgs->metadata_resv = metadata_resv;
    bookkeepArgs->mainThreadState = mainThreadState;
    bookkeepArgs->cutoff_limit = cutoff_limit;
    // long thread_id = PyThread_start_new_thread(thread_trace_from_gc_list, (void *)bookkeepArgs);
    // long thread_id = PyThread_start_new_thread(thread_trace_from_refchain, (void *)bookkeepArgs); // #ifdef Py_TRACE_REFS
    // long thread_id = PyThread_start_new_thread(trace_total_hotness, (void *)bookkeepArgs);
    // long thread_id = PyThread_start_new_thread(use_pref_cnt_modified, (void *)bookkeepArgs);
    long thread_id = PyThread_start_new_thread(manual_trigger_scan, (void *)bookkeepArgs);
    // long thread_id = PyThread_start_new_thread(use_utlist, (void *)bookkeepArgs);
    // long thread_id = PyThread_start_new_thread(inspect_survived_objs, (void *)bookkeepArgs);
    // long thread_id = PyThread_start_new_thread(trace_global_live_op_gc, (void *)bookkeepArgs);
    // long thread_id = PyThread_start_new_thread(test_enable_tracing_in_gc_main, (void *)bookkeepArgs);
    if (thread_id == -1)
    {
        perror("thread spawn error\n");
        return NULL; // error
    }
    Py_RETURN_NONE;
}

void *print_get_sizeof_start_routine(void *arg)
{
    PyObject *py_list = (PyObject *)arg;
    while (!terminate_flag_refchain)
    {
        PyGILState_STATE gstate = PyGILState_Ensure();
        PyObject_Print(py_list, stdout, 0);
        fprintf(stderr, "list: %zu\t%ld\n", _PySys_GetSizeOf(py_list), _PySys_GetSizeOf(py_list));
        for (int i = 0; i < PyList_Size(py_list); i++)
        {
            PyObject *item = PyList_GetItem(py_list, i);
            fprintf(stderr, "obj: %zu\t%ld\n", _PySys_GetSizeOf(item), _PySys_GetSizeOf(item));
        }
        PyGILState_Release(gstate);
        sleep(1);
    }
    sleep(1);
    terminate_flag_refchain = 0;
    fprintf(stderr, "finish dummy\n");
}

static PyObject *print_get_sizeof(PyObject *self, PyObject *args)
{
    PyObject *pyList = PyList_New(0);
    if (!pyList)
    {
        PyErr_Print();
        return 1;
    }
    for (long i = 0; i < 5; ++i)
    {
        PyObject *pyLong = PyLong_FromLong(i);
        if (!pyLong)
        {
            PyErr_Print();
            Py_DECREF(pyList);
            return 1;
        }
        PyList_Append(pyList, pyLong);
        Py_DECREF(pyLong);
    }
    PyObject *pyString = PyUnicode_FromString("Hello, World!");
    PyList_Append(pyList, pyString);
    long thread_id = PyThread_start_new_thread(print_get_sizeof_start_routine, (void *)pyList);
    if (thread_id == -1)
    {
        perror("thread spawn error\n");
        return NULL; // error
    }
    Py_RETURN_NONE;
}

static PyObject *close_count_gc_list(PyObject *self, PyObject *args)
{
    // terminate_flag = 1;
    terminate_flag_refchain = 1;
    fprintf(stderr, "stop bk, but should continue flushing111...\n");
    fflush(stderr);
    // sleep(1);
    long thread_id = PyThread_start_new_thread(sleep_thread_and_close_fd, NULL);
    if (thread_id == -1)
    {
        perror("thread spawn error\n");
        return NULL; // error
    }
    // usleep(50000000); // sleep 60s waiting for flushing
    Py_RETURN_NONE;
}

static PyMethodDef ThreadMethods_[] = {
    {"print_get_sizeof", print_get_sizeof, METH_NOARGS, "print get sizeof"},
    {"start_count_gc_list", start_count_gc_list, METH_VARARGS, "Start a thread counting from gc list."},
    {"close_count_gc_list", close_count_gc_list, METH_NOARGS, "Close the counting thread."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef gc_count_module = {
    PyModuleDef_HEAD_INIT,
    "gc_count_module",
    NULL,
    -1,
    ThreadMethods_};

PyMODINIT_FUNC PyInit_gc_count_module(void)
{
    return PyModule_Create(&gc_count_module);
}
