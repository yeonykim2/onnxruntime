#!/bin/sh
Name:           onnxruntime
Summary:        ONNXRuntime 1.x
Version:        1.16.3
Release:        1
License:        MIT
Source0:        %{name}-%{version}.tar.gz
Source1001:     onnxruntime.manifest
Source1002:     libonnxruntime.pc.in
Source2001:     abseil-cpp.tar.gz
Source2002:     date.tar.gz
Source2003:     eigen-3.4.1.tar.gz
Source2004:     flatbuffers.tar.gz
Source2005:     google_nsync.tar.gz
Source2006:     microsoft_gsl.tar.gz
Source2007:     mp11.tar.gz
Source2008:     nlohmann_json.tar.gz
Source2010:     onnx.tar.gz
Source2011:     protobuf.tar.gz
Source2012:     pytorch_cpuinfo.tar.gz
Source2013:     re2.tar.gz
Source2014:     safeint.tar.gz

Source10001:    0001-change-external-source-path.patch
Source10002:    0002-change-cmakelists-patch.patch

BuildRequires: cmake
BuildRequires: ninja
BuildRequires:	python3
BuildRequires:	python3-devel

%description
ONNX Runtime is a cross-platform inference and training machine-learning accelerator.
ONNX Runtime inference can enable faster customer experiences and lower costs, supporting models from deep learning frameworks such as PyTorch and TensorFlow/Keras as well as classical machine learning libraries such as scikit-learn, LightGBM, XGBoost, etc. ONNX Runtime is compatible with different hardware, drivers, and operating systems, and provides optimal performance by leveraging hardware accelerators where applicable alongside graph optimizations and transforms.
ONNX Runtime training can accelerate the model training time on multi-node NVIDIA GPUs for transformer models with a one-line addition for existing PyTorch training scripts.

%package devel
Summary: ONNX Runtime development headers and object file

%description devel
ONNX Runtime development headers and object file

%define SHARED_LIB    "ON"
%define DISABLE_SPARSE_TENSORS "OFF"

%prep
%setup
cp %{SOURCE1001} .
patch -p1 < %{SOURCE10001}
patch -p1 < %{SOURCE10002}

mkdir -p cmake/externals
pushd cmake/externals
cp %{SOURCE2001} .
cp %{SOURCE2002} .
cp %{SOURCE2003} .
cp %{SOURCE2004} .
cp %{SOURCE2005} .
cp %{SOURCE2006} .
cp %{SOURCE2007} .
cp %{SOURCE2008} .
cp %{SOURCE2010} .
cp %{SOURCE2011} .
cp %{SOURCE2012} .
cp %{SOURCE2013} .
cp %{SOURCE2014} .
popd

pushd cmake
cp %{SOURCE1002} .
sed -i 's:@libdir@:%{_libdir}:g
    s:@includedir@:%{_includedir}/onnxruntime/:g' ./libonnxruntime.pc.in
popd

%build
mkdir -p build
pushd build

# To fix the buildbreak issue on gcc 11 or higher,
# '-Wno-error=stringop-overflow' option is added to CFLAGS and CXXFLAGS.
EXTRA_CFLAGS="${CFLAGS} -Wno-error=stringop-overflow"
EXTRA_CXXFLAGS="${CXXFLAGS} -Wno-error=stringop-overflow"

%ifarch %arm aarch64
EXTRA_CFLAGS="${EXTRA_CFLAGS} -Wno-error=attributes"
EXTRA_CXXFLAGS="${EXTRA_CXXFLAGS} -Wno-error=attributes"
  %ifarch %arm
    %define DISABLE_SPARSE_TENSORS "ON"
  %endif
%endif
# EXTRA_CFLAGS="${EXTRA_CFLAGS} -Wno-error=attributes -Wno-psabi -ffunction-sections -fdata-sections -Wnon-virtual-dtor"
# EXTRA_CXXFLAGS="${EXTRA_CXXFLAGS} -Wno-error=attributes -Wno-psabi"

# EXTRA_CFLAGS="${EXTRA_CFLAGS} -mfloat-abi=softfp -march=armv7-a -mfpu=neon-vfpv4 -funsafe-math-optimizations -mfp16-format=ieee"
# EXTRA_CXXFLAGS="${EXTRA_CXXFLAGS} -mfloat-abi=softfp -march=armv7-a -mfpu=neon-vfpv4 -funsafe-math-optimizations -mfp16-format=ieee"

# EXTRA_CFLAGS="${EXTRA_CFLAGS} -latomic -std=c++17 -Wno-error=attributes"
# EXTRA_CXXFLAGS="${EXTRA_CXXFLAGS} -latomic -std=c++17 -Wno-error=attributes"

# EXTRA_CFLAGS="${EXTRA_CFLAGS} -fassociative-math -ffast-math -ftree-vectorize -funsafe-math-optimizations -mfpu=neon -march=armv8.2-a+fp16 "
# EXTRA_CXXFLAGS="${EXTRA_CXXFLAGS} -fassociative-math -ffast-math -ftree-vectorize -funsafe-math-optimizations -mfpu=neon -march=armv8.2-a+fp16 "

  # -GNinja \

cmake \
  -GNinja \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_FLAGS="${EXTRA_CFLAGS}" \
  -DCMAKE_CXX_FLAGS="${EXTRA_CXXFLAGS}" \
  -Donnxruntime_BUILD_SHARED_LIB="%{SHARED_LIB}" \
  -Donnxruntime_DISABLE_SPARSE_TENSORS="%{DISABLE_SPARSE_TENSORS}" \
  -Donnxruntime_BUILD_UNIT_TESTS=OFF \
  ../cmake
#   -Donnxruntime_ENABLE_LTO=ON \ -DCMAKE_SYSTEM_PROCESSOR=armv7 \   # -Donnxruntime_ENABLE_CPUINFO=OFF \
cmake --build . %{?_smp_mflags} #--target install
popd
#make install

%install
# make
# DESTDIR=%{?buildroot} make install

mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}/onnxruntime
# mkdir -p %{buildroot}%{_bindir}
#mkdir -p %{buildroot}%{_datadir}/onnxruntime/schema
#pushd %{buildroot}%{_includedir}/onnxruntime
#ln -sf . %{buildroot}%{_includedir}/onnxruntime
## ONNX Runtime users do: #include <core/session/onnxruntime_cxx_api.h>
#popd


# Put the generated files into the buildroot folder
## install built static library and benchmark binary
%if %{SHARED_LIB} == "ON"
 install -m 0644 ./build/libonnxruntime.so* %{buildroot}%{_libdir}/
%else
#  cp ./build/*.a %{buildroot}%{_libdir}/
 install -m 0644 ./build/*.a %{buildroot}%{_libdir}/
%endif


## install headers
pushd include/onnxruntime/core/session
find . -name "*.h" -type f -exec cp --parents {} %{buildroot}%{_includedir}/onnxruntime \;
popd
#popd

## install pc file
install -m 0644 ./build/libonnxruntime.pc %{buildroot}%{_libdir}/pkgconfig/libonnxruntime.pc
# install -m 0644 %{SOURCE1001} %{buildroot}
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root,-)
%manifest onnxruntime.manifest
%license LICENSE
%if %{SHARED_LIB} == "ON"
  %{_libdir}/libonnxruntime.so*
%else
  %{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/libonnxruntime.pc
%{_includedir}/onnxruntime


%changelog
* Mon Nov 28 2022 Suyeon Kim <suyeon5.kimn@samsung.com>
 - Initial package te use ONNX Runtime v1.16.0
