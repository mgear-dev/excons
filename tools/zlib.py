# Copyright (C) 2014  Gaetan Guidet
#
# This file is part of excons.
#
# excons is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or (at
# your option) any later version.
#
# excons is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

from SCons.Script import *
import excons

def GetOptionsString():
  return """ZLIB OPTIONS
  with-zlib=<path>     : Zlib prefix.
  with-zlib-inc=<path> : Zlib headers directory.           [<prefix>/include]
  with-zlib-lib=<path> : Zlib libraries directory.         [<prefix>/lib]
  zlib-static=0|1      : Link Zlib statically.             [0]
  zlib-libname=<str>   : Override Zlib library name.       []
  zlib-libsuffix=<str> : Default Zlib library name suffix. []
                         (ignored when zlib-libname is set)
                         (default name is 'z' on osx and linux, 'zlib' (static) or 'zdll' (shared) on windows)"""

def Require(env):
  zlibinc, zliblib = excons.GetDirs("zlib")
  
  if zlibinc:
    env.Append(CPPPATH=[zlibinc])
  
  if zliblib:
    env.Append(LIBPATH=[zliblib])
  
  static = (excons.GetArgument("zlib-static", 0, int) != 0)

  if str(Platform()) != "win32":
    zlib_name = excons.GetArgument("zlib-libname", None)
    if not zlib_name:
      zlib_name = "z%s" % excons.GetArgument("zlib-libsuffix", "")
    
    if not static or not excons.StaticallyLink(env, zlib_name):
      env.Append(LIBS=[zlib_name])
  
  else:
    if static:
      zlib_name = excons.GetArgument("zlib-libname", None)
      if not zlib_name:
        zlib_name = "zlib%s" % excons.GetArgument("zlib-libsuffix", "")
      
      env.Append(LIBS=[zlib_name])
    
    else:
      zlib_name = excons.GetArgument("zlib-libname", None)
      if not zlib_name:
        zlib_name = "zdll%s" % excons.GetArgument("zlib-libsuffix", "")
      
      env.Append(CPPDEFINES=["ZLIB_DLL"])
      env.Append(LIBS=[zlib_name])
  
  excons.AddHelpOptions(zlib=GetOptionsString())
