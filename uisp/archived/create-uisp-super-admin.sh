# For creating Super Admins on UNMS before version 1.2
docker exec -it unms-postgres psql -U unms
INSERT INTO unms.user (id,username,email,password,role) VALUES ('2eb74762-1d0d-11ea-978f-2e728cb88175','hsuperadmin','support@hostifi.com','$2a$10$mPGNa6OpXV61o7T6qfxOauhEXuW4jVEggi1JXd498XPM/oqrSS07i','superadmin');
\q
echo "UNMS Super Admin created!"
echo "Username: hsuperadmin"
echo "Password: RandomHost2!"