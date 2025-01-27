# YappDown
A note taking app built in Django on Alpine Linux with Mariadb and TailwindCSS using Docker.

### Required
Alpine Linux,
Django,
Mariadb,
Docker.

### Personal choices
TailwindCSS: uses utility-first classes to apply styles directly in the HTML, resulting in smaller and more maintainable stylesheets

## Compile and Run
### Automatically (recommended)
```sh
chmod +x yappdown.sh
```
and
```sh
./yappdown.sh
```
or
```sh
bash yappdown.sh
```

### Manually compile 
#### Build:
    docker build -t yappdown . --network=host
#### Run:
##### Docker Image:
    docker run -p 8000:8000 yappdown
##### OR Docker Container:
    docker run -d -p 8000:8000 --name yappdown-container yappdown
#### Stop (Docker Image):
Find the Image with the name "yappdown" or what you named it:  

    docker ps
Stop the Image (replace "container_id_or_name" with the actual containers ID or Name):  

    docker stop <container_id_or_name>

#### Stop (Docker Container):
```sh
docker stop yappdown-container
docker rm yappdown-container
```

#### Check logs:
```sh
docker logs yappdown-container
```

### Known Startup Issues:
If Docker run returns an issue saying it expects "then" or "fi" in the "starter.sh" file, make sure the "End Of Line Sequence" is set to "LF" and not "CRLF" for "starter.sh".

## Demonstration

1. Register a user with a username and password. (For admin make the username "Admin")
2. You will automatically be brought to the Home page
Main Page:
Here you may see your storage information: used, left and allocated(10mb per user).
You will also see all your previously made notes here.
3. Click New Note
Here you will see a navigation on the left to take you home and show all your notes.
The center shows either creating a new note or the details of a selected note for updating.
You may also upload a file as a note (pdf, docx, txt)
4. Add a note Titled "YappDown" and content "A note taking app built on Django."
5. You will now see a note titled "YappDown" on the left navigation.
6. Click on the note "YappDown" in the left navigation.
7. You will now see the notes details including the date it was created and updated as well as a "Remove Note" button.
8. Click the "Home" button in the top left corner
9. You will now see the note we just created and its details.
10. Click "Edit" on the note.
11. Click the "Remove Note" button
12. You will notice we have returned to the main screen
13. If you are not an Admin please click "Logout" in the top left corner, if you are an Admin proceed to step 15.
14. Register as an Admin (See step 1)
15. You will notice an "Admin" button in the top left corner under the "Logout" button, click the "Admin" button.
16. This is the Admin page.
Here you can see the "Total Storage Used", "Disk Storage Left", "Cpu Usage" and a searchable table of users.
As an admin you have the ability to revoke a users access to the application and grant it back. This will not remove access entirely, the user will just not be able to view, create or edit notes.
17. Remove your access, (remove "Admin"s access)
18. Return to the home page with the button "Home" in the top left corner.
19. Notice the "Access Denied" notification and no "New Note" button.

This concludes the demonstration of YappDown.