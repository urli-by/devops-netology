1.	Допиливаем конфиг вагранта под нужды
# -*- mode: ruby -*-
# vi: set ft=ruby :

boxes = {
  'net' => '11',
}

Vagrant.configure("2") do |config|
   config.vm.box = "bento/centos-7.7"
  config.vm.network "forwarded_port", guest: 8200, host: 8200
  config.vm.network "private_network", virtualbox__intnet: true, auto_config: false
 
  boxes.each do |k, v|
    config.vm.define k do |node|
      node.vm.provision "shell" do |s|
        s.inline = "hostname $1;"\
			"ip addr add $2 dev eth1;"\
			"ip link set dev eth1 up;"\
			"sudo yum update;"\
			"sudo yum -y install net-tools epel-release yum-utils;"\
			"sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo;"\
			"sudo yum -y install jq;"\
			"sudo yum -y install vault"	
		  
        s.args = [k, "172.28.128.#{v}/24"]
      end
    end
  end

end
2.	Скачиваем и правим конфиг nginx
     #HTTPS server
    server {
		listen 443 ssl;
		server_name netology.example.com www.netology.example.com;
		
		root  html;
		index index.html index.htm;
		
		ssl_certificate      ssl/netology.example.com.crt.pem;
		ssl_certificate_key  ssl/netology.example.com.crt.key;
		ssl_ciphers          "HIGH:!RC4:!aNULL:!MD5:!kEDH";
		
		location / {
		try_files $uri $uri/ =404;
			}
}
3.	Запускаем vault в режиме dev
[root@localhost ~]# vault server -dev
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.15.11
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.7.2
             Version Sha: db0e4245d5119b5929e611ea4d9bf66e47f3f208

==> Vault server started! Log data will stream in below:
4.	Следуя инструкции создаем CA и Inermediate CA
[root@localhost ~]# export VAULT_ADDR=https://127.0.0.1:8200
[root@localhost ~]# export VAULT_ADDR=http://127.0.0.1:8200
[root@localhost ~]# export VAULT_TOKEN=s.CY3FkHCw4Mkku40APA53kj7M
[root@localhost ~]# vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/
[root@localhost ~]# vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/
[root@localhost ~]# vault write -field=certificate pki/root/generate/internal \
>         common_name="example.com" \
>         ttl=87600h > CA_cert.crt
[root@localhost ~]# vault write pki/config/urls \
>         issuing_certificates="$VAULT_ADDR/v1/pki/ca" \
>         crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
Success! Data written to: pki/config/urls

[root@localhost ~]# vault secrets enable -path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/
[root@localhost ~]# vault secrets tune -max-lease-ttl=43800h pki_int
Success! Tuned the secrets engine at: pki_int/
[root@localhost ~]# vault write -format=json pki_int/intermediate/generate/internal \
>         common_name="example.com Intermediate Authority" \
>         | jq -r '.data.csr' > pki_intermediate.csr
[root@localhost ~]# vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr \
>         format=pem_bundle ttl="43800h" \
>         | jq -r '.data.certificate' > intermediate.cert.pem
[root@localhost ~]# vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed

Создаем роль
[root@localhost ~]# vault write pki_int/roles/example-dot-com \
>         allowed_domains="example.com" \
>         allow_subdomains=true \
>         max_ttl="720h"
Success! Data written to: pki_int/roles/example-dot-com

Выпускаем сертификат для нашего прокси

vault write pki_int/issue/example-dot-com \
common_name="test.example.com" \
alt_names="netology.example.com" \
ttl="43800h" > netology.example.com.crt

Добываем из него файлик .key через блокнот 
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN RSA PRIVATE KEY-----

netology.example.com.crt.pem
certificate 
issuing ca

5.	Копируем эти файлы в папку nginx
6.	Добавляем наш intermediate_ca в трастед 
[root@localhost ~]# cp intermediate.cert.pem  /etc/pki/ca-trust/source/anchors/
[root@localhost ~]# update-ca-trust extract

7.	[root@localhost ~]# curl -I -s https://netology.example.com | head -n1
HTTP/1.1 200 OK

Иногда казалось, что эта домашка будет продолжаться вечно и я никогда не смогу её доделать (((
