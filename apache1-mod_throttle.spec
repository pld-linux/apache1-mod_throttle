%define 	apxs	/usr/sbin/apxs
Summary:	Bandwidth & Request Throttling for Apache
Summary(cs):	Omezen� s��ov�ho provozu pro Apache
Summary(de):	Ein Modul, das die Bandbreiten- und Anforderungseinschr�nkung f�r Apache implementiert
Summary(es):	M�dulo que implementa la gesti�n de ancho de banda y peticiones para Apache
Summary(fr):	Module qui met en oeuvre la bande passante et l'�tranglement requis pour Apache
Summary(it):	Modulo che implementa la larghezza di banda e la richiesta di throttling per Apache
Summary(ja):	Apache ���Ӱ���������׵᥹���åȥ���������⥸�塼��
Summary(pl):	T�umienie przepustowo�ci i zapyta� dla Apache'a
Summary(pt_BR):	Descompress�o "On-the-fly" de arquivos HTML para o Apache
Summary(sv):	En modul som implementerar bandvidd- och beg�ranbegr�nsningar i Apache
Name:		apache-mod_throttle
Version:	3.1.2
Release:	6
License:	Anthony Howe
Group:		Networking/Daemons
Source0:	http://www.snert.com/Software/mod_throttle/mod_throttle312.tgz
# Source0-md5:	6edc45c3ea8a0855d4b0b14cf0f76404
Patch0:		%{name}-PLD-v6stuff.patch
URL:		http://www.snert.com/Software/mod_throttle/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache >= 1.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _libexecdir     %{_libdir}/apache
%define         _htmldocdir     /home/httpd/manual/mod

%description
This Apache module is intended to reduce the load on your server &
bandwidth generated by popular virtual hosts, directories, locations,
or users according to supported polices (see below) that decide when
to delay or refuse requests. Also mod_throttle can track and throttle
incoming connections by IP address or by authenticated remote user.

%description -l cs
Bal��ek mod_throttle obsahuje modul, kter� umo��uje omezit pr�tok dat,
kter� odch�zej� z WWW serveru Apache. Limity mohou b�t nastaveny pro
jednotliv� virtu�ln� weby, adres��e, um�st�n� nebo autentizovan�
u�ivatele.

%description -l de
Mod_throttle kann verwendet werden, um die Datenmenge zu beschr�nken,
die Ihr Web-Server behandelt. Diese Einschr�nkungen k�nnen f�r
einzelne virtuelle Rechner, Verzeichnisse, Speicherstellen oder
authentifizierte Benutzer eingestellt werden.

%description -l es
Mod_throttle puede usarse para limitar la cantidad de datos que su
servidor web va a servir. Estos l�mites se pueden configurar para
hosts virtuales individuales, directorios, lug<res o usuarios
autenticados.

%description -l fr
Mod_throttle peut �tre utilis� pour limiter la quantit� de donn�es
servies par votre serveur Web. Ces limites peuvent �tre d�finies pour
des h�tes virtuels individuels, r�pertoires, emplacements ou
utilisateurs authentifi�s.

%description -l it
Mod_throttle pu� essere usato per limitare la quantit� di dati che il
server Web dovr� servire. Queste limitazioni possono essere
configurate per singoli host virtuali, directory, indirizzi o utenti
autenticati.

%description -l ja
Mod_throttle �ˤ�ä� Web �����С�����������ǡ����̤����¤Ǥ��ޤ�
���������¤ϡ��ġ��β��ۥۥ��ȡ��ǥ��쥯�ȥꡢ��ꡢ�ޤ���
ǧ�ڥ桼�����ѤˤĤ�������Ǥ��ޤ���

%description -l pl
Ten modu� Apache ma s�u�y� do zmniejszania obci��enia serwera i ruchu
generowanego przez popularne hosty wirtualne, katalogi, pliki lub
u�ytkownik�w zgodnie z obs�ugiwanymi polisami, kt�re decyduj� kiedy
op�ni� lub odrzuci� zapytanie. mod_throttle mo�e tak�e �ledzi� i
t�umi� po��czenia przychodz�ce z danego adresu IP lub danego,
autentykuj�cego si�, u�ytkownika.

%description -l pt_BR
Descompress�o "On-the-fly" de arquivos HTML para o Apache.

%description -l sv
Mod_throttle kan anv�ndas f�r att begr�nsa m�ngden data som din
webbserver skickar. Dessa gr�nser kan s�ttas f�r enskilda virtuella
v�rdar, kataloger, platser eller autenticerade anv�ndare.

%prep
%setup -q -n mod_throttle-%{version}
%patch0 -p1

%build
%{apxs} -DSUEXEC_BIN="\"\\\"%{_sbindir}/suexec\\\"\"" -o mod_throttle.so -c mod_throttle.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_htmldocdir}}

install mod_throttle.so $RPM_BUILD_ROOT%{_libexecdir}

sed -e 's/<!--#/<!--/g' index.shtml > mod_throttle.html

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n throttle %{_libexecdir}/mod_throttle.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n throttle %{_libexecdir}/mod_throttle.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.txt *.html
%attr(755,root,root) %{_libexecdir}/*
