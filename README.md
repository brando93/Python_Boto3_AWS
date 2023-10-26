# Python_Boto3_AWS
Python BOTO3 script (IAM,EC2, S3)

yum install gcc
yum install openssl-devel
yum install bzip2-devel
yum install libffi-devel
cd /usr/src
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
ll | grep Python
rm -rf Python-3.7.4.tgz 
mv /tmp/Python-3.7.4.tgz .
tar xzf Python-3.7.4.tgz
cd Python-3.7.4/
/configure --enable-optimizations
make altinstall
cd /usr/local/bin/
./python3.7 --version
./pip3.7 --version
pwd
ln -s /usr/local/bin/python3.7 /bin/python3
python3 --version
ln -s /usr/local/bin/pip3.7 /bin/pip3
pip3 install boto3![image](https://github.com/brando93/Python_Boto3_AWS/assets/45773752/a01d5e09-7be6-49bb-bca5-d2886967a23b)
