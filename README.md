<h1>Astronomical Event Alert System</h1>

![Screenshot 2025-06-03 163510](https://github.com/user-attachments/assets/fd623717-1456-4a1f-93bb-c7d642bfbc54)

<h4>The project follows a client-server model:</h4>
<ul>
  <li>Backend: Python Flask server (handles data processing/APIs)</li>
  <li>Frontend: HTML/CSS/JavaScript interface (displays events)</li>
</ul>
<h4>Backend processing:</h4><br>
graph TD<br>
A[Receive request] --> B[Fetch from NASA API]<br>
B --> C[Fetch Meteor Shower data]<br>
C --> D[Filter by location/time]<br>
D --> E[Return JSON response]<br>

<h4>Key Python Functionalities Used</h4>
<ul>
  <li> Web Framework: Flask</li>
  <li>API Integration</li>
  <ul>
    <li>NASA's Close Approach API (asteroid data)</li>
    <li>Meteor Shower API (meteor shower schedules)</li>
  </ul>
 
</ul>
<h3>How to Run the Full Application</h3>
<h5>1.Install dependencies:</h5>
<ul>
  <li>pip install flask flask-cors requests geocoder timezonefinder pytz ics</li>
</ul>
<h5>Create the project structure:</h5>
<ul>
  <li>
    skywatch-app/ <br>
├── app.py<br>
└── templates/<br>
    └── index.html<br>
  </li>
  
</ul>
<h5>Run the application in vs code terminal:</h5>
<ul>
  <li>python app.py</li>
</ul>
<h5>Access the application:</h5>
<ul>
  <li>Open your browser and go to http://localhost:5000</li>
</ul>


