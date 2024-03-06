add ssh comination with gitlab

1. Go to "Git Bash" just like cmd. Right click and "Run as Administrator".
2. Type ssh-keygen
3. Press enter.
4. It will ask you to save the key to the specific directory.
5. Press enter. It will prompt you to type password or enter without password.
6. The public key will be created to the specific directory.
7. Now go to the directory and open .ssh folder.
8. You'll see a file id_rsa.pub. Open it on notepad. Copy all text from it.
9. Go to https://gitlab.com/-/profile/keys or
10. Paste here in the "key" textfield.
11. Now click on the "Title" below. It will automatically get filled.
12. Then click "Add key".

Django:
`https://docs.djangoproject.com/en/4.0/`

docker and docker compose are required to run the database

command:
`docker-compose -f docker-compose.dev.yml up -d`

the database will launch on port `6002`