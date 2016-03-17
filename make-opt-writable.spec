Summary:    Make /opt writable during the RPM build phase
Name:       make-opt-writable
Version:    1.0.0
Release:    1
License:    WTFPL
Vendor:     Immobilien Scout GmbH
Packager:   Valentin Haenel
Group:      is24
Source0:    %{name}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-root
BuildArch:  noarch

%description
Makes the directory /opt in the buildroot world writable so that other packages
can install things into it.

%prep

%build

%install

%files

%post
chmod 1777 /opt
