========================
Python on watchOS README
========================

:Authors:
    Russell Keith-Magee (2023-11)

This document provides a quick overview of some watchOS specific features in the
Python distribution.

Compilers for building on watchOS
=================================

Building for watchOS requires the use of Apple's Xcode tooling. It is strongly
recommended that you use the most recent stable release of Xcode, on the
most recently released macOS.

watchOS specific arguments to configure
=======================================

* ``--enable-framework[=DIR]``

  This argument specifies the location where the Python.framework will
  be installed.

* ``--with-framework-name=NAME``

  Specify the name for the python framework, defaults to ``Python``.


Building and using Python on watchOS
====================================

ABIs and Architectures
----------------------

watchOS apps can be deployed on physical devices, and on the watchOS simulator.
Although the API used on these devices is identical, the ABI is different - you
need to link against different libraries for an watchOS device build
(``watchos``) or an watchOS simulator build (``watchsimulator``). Apple uses the
XCframework format to allow specifying a single dependency that supports
multiple ABIs. An XCframework is a wrapper around multiple ABI-specific
frameworks.

watchOS can also support different CPU architectures within each ABI. At present,
there is only a single support ed architecture on physical devices - ARM64.
However, the *simulator* supports 2 architectures - ARM64 (for running on Apple
Silicon machines), and x86_64 (for running on older Intel-based machines.)

To support multiple CPU architectures on a single platform, Apple uses a "fat
binary" format - a single physical file that contains support for multiple
architectures.

How do I build Python for watchOS?
-------------------------------

The Python build system will build a ``Python.framework`` that supports a
*single* ABI with a *single* architecture. If you want to use Python in an watchOS
project, you need to:

1. Produce multiple ``Python.framework`` builds, one for each ABI and architecture;
2. Merge the binaries for each architecture on a given ABI into a single "fat" binary;
3. Merge the "fat" frameworks for each ABI into a single XCframework.

watchOS builds of Python *must* be constructed as framework builds. To support this,
you must provide the ``--enable-framework`` flag when configuring the build.

The build also requires the use of cross-compilation. The commands for building
Python for watchOS will look somethign like::

  $ ./configure \
        --enable-framework=/path/to/install \
        --host=aarch64-apple-watchos \
        --build=aarch64-apple-darwin \
        --with-build-python=/path/to/python.exe
  $ make
  $ make install

In this invocation:

* ``/path/to/install`` is the location where the final Python.framework will be
  output.

* ``--host`` is the architecture and ABI that you want to build, in GNU compiler
  triple format. This will be one of:

  - ``arm64_32-apple-watchos`` for ARM64-32 watchOS devices.
  - ``aarch64-apple-watchos-simulator`` for the watchOS simulator running on Apple
    Silicon devices.
  - ``x86_64-apple-watchos-simulator`` for the watchOS simulator running on Intel
    devices.

* ``--build`` is the GNU compiler triple for the machine that will be running
  the compiler. This is one of:

  - ``aarch64-apple-darwin`` for Apple Silicon devices.
  - ``x86_64-apple-darwin`` for Intel devices.

* ``/path/to/python.exe`` is the path to a Python binary on the machine that
  will be running the compiler. This is needed because the Python compilation
  process involves running some Python code. On a normal desktop build of
  Python, you can compile a python interpreter and then use that interpreter to
  run Python code. However, the binaries produced for watchOS won't run on macOS, so
  you need to provide an external Python interpreter. This interpreter must be
  the version as the Python that is being compiled.

Using a framework-based Python on watchOS
======================================
