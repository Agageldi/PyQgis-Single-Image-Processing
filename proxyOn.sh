if [ $(id -u) -ne 0 ]; then
  echo "This script must be run as root";
  exit 1;
fi
 
if [ $# -eq 4 ]
  then
 
#  gsettings set org.gnome.system.proxy mode 'manual' ;
#  gsettings set org.gnome.system.proxy.http host '$3';
#  gsettings set org.gnome.system.proxy.http port $4;
 
 
  grep PATH /etc/environment > lol.t;
  printf \
  "http_proxy=http://$1:$2@$3:$4/\n\
  https_proxy=http://$1:$2@$3:$4/\n\
  ftp_proxy=http://$1:$2@$3:$4/\n\
  no_proxy=\"localhost,127.0.0.1,localaddress,.localdomain.com\"\n\
  HTTP_PROXY=http://$1:$2@$3:$4/\n\
  HTTPS_PROXY=http://$1:$2@$3:$4/\n\
  FTP_PROXY=http://$1:$2@$3:$4/\n\
  NO_PROXY=\"localhost,127.0.0.1,localaddress,.localdomain.com\"\n" >> lol.t;
 
  cat lol.t > /etc/environment;
 
 
  printf \
  "Acquire::http::proxy \"http://$1:$2@$3:$4/\";\n\
  Acquire::ftp::proxy \"ftp://$1:$2@$3:$4/\";\n\
  Acquire::https::proxy \"https://$1:$2@$3:$4/\";\n" > /etc/apt/apt.conf.d/95proxies;
 
  rm -rf lol.t;
 
  else
 
  printf "Usage $0 <user> <password> <proxy_ip> <proxy_port>\n";
 
fi