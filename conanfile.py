from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from shutil import copyfile
import os

class SbcConan(ConanFile):
    name = "sbc"
    version = "1.3"
    description = "SBC is a digital audio encoder and decoder used to transfer data to Bluetooth audio output devices like headphones or loudspeakers"
    url = "https://github.com/conan-multimedia/sbc"
    wiki = 'https://en.wikipedia.org/wiki/SBC_(codec)'
    license = "LGPLv2_1Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        #'http://www.kernel.org/pub/linux/bluetooth/sbc-1.3.tar.gz'
        url_ = "http://172.16.64.65:8081/artifactory/gstreamer/{name}-{version}.tar.gz".format(name=self.name, version=self.version)
        tools.get(url_.format(version =self.version))
        os.rename(self.name + "-" + self.version, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            _args = ["--prefix=%s/builddir"%(os.getcwd()), "--disable-tester", "--disable-tools", "--disable-silent-rules"]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

