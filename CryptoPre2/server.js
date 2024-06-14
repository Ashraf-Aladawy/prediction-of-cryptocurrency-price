const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const nodemailer = require("nodemailer");
const mysql = require("mysql");
const session = require("express-session");
const bcrypt = require("bcrypt");
const cors = require("cors");

// Create express app
const app = express();

// Middleware setup
app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public"))); // Use 'public' folder for static files

// Set up session middleware
app.use(
  session({
    secret: "web session",
    resave: true,
    saveUninitialized: true,
  })
);

// CORS configuration
app.use(
  cors({
    origin: "http://127.0.0.1:5050", // Allow requests from this origin
    credentials: true, // Allow cookies and other credentials to be sent
  })
);

// Database connection
const con = mysql.createConnection({
  host: "localhost",
  database: "cryptopre",
  user: "root",
  password: "",
});

con.connect((error) => {
  if (error) {
    console.error("Error connecting to database:", error);
    process.exit(1);
  } else {
    console.log("MySQL database connected successfully");
  }
});

// Middleware to protect routes
function requireAuth(req, res, next) {
  if (req.session && req.session.userId) {
    next();
  } else {
    res.redirect("/login.html");
  }
}

// Register route
app.post("/register", async (req, res) => {
  const { name, email, password } = req.body;

  if (!name || !email || !password) {
    return res.status(400).send("All fields are required.");
  }

  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    const sql = "INSERT INTO user (name, email, password) VALUES (?, ?, ?)";
    con.query(sql, [name, email, hashedPassword], (err, result) => {
      if (err) {
        console.error("Error inserting user into database:", err);
        return res
          .status(500)
          .send("An error occurred while registering the user.");
      } else {
        res.status(201).json({ message: "User registered successfully" });
      }
    });
  } catch (error) {
    console.error("Error hashing password:", error);
    res.status(500).send("An error occurred while processing your request.");
  }
});

// Login route
app.post("/login", (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).send("Email and password are required.");
  }

  const sql = "SELECT * FROM user WHERE email = ?";
  con.query(sql, [email], async (err, results) => {
    if (err) {
      console.error("Error fetching user from database:", err);
      return res.status(500).send("An error occurred while logging in.");
    }

    if (results.length === 0) {
      return res.status(401).json({ message: "Invalid email or password." });
    }

    const user = results[0];
    const match = await bcrypt.compare(password, user.password);

    if (match) {
      // Create a session record in the database
      const sessionId = req.sessionID; // Get the session ID
      const userId = user.id;

      const sessionSql =
        "INSERT INTO sessions (session_id, user_id) VALUES (?, ?)";
      con.query(
        sessionSql,
        [sessionId, userId],
        (sessionErr, sessionResult) => {
          if (sessionErr) {
            console.error("Error creating session in database:", sessionErr);
            return res.status(500).send("An error occurred while logging in.");
          }
        }
      );

      // Set session variables
      req.session.userId = user.id;
      req.session.userName = user.name;
      req.session.userEmail = user.email;

      res.status(200).json({ message: "Login successful", user_id: user.id });
    } else {
      res.status(401).json({ message: "Invalid email or password." });
    }
  });
});

// Reset password route
app.post("/reset-password", async (req, res) => {
  const { email, newPassword } = req.body;

  if (!email || !newPassword) {
    return res.status(400).send("Email and new password are required.");
  }

  try {
    const hashedPassword = await bcrypt.hash(newPassword, 10);
    const sql = "UPDATE user SET password = ? WHERE email = ?";
    con.query(sql, [hashedPassword, email], (err, result) => {
      if (err) {
        console.error("Error updating password in database:", err);
        return res
          .status(500)
          .send("An error occurred while updating the password.");
      } else {
        res.send("Password updated successfully.");
      }
    });
  } catch (error) {
    console.error("Error hashing password:", error);
    res.status(500).send("An error occurred while processing your request.");
  }
});

// Contact us route
app.post("/name", (req, res) => {
  const { name, email, phone, message } = req.body;

  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      user: "cryptopre2025@gmail.com",
      pass: "qqlc vxsr lebj kuge",
    },
  });

  const mailOptions = {
    from: "cryptopre2025@gmail.com",
    to: "cryptopre2024@gmail.com",
    subject: "Message from Your Website",
    html: `<p>Name: ${name}</p><p>Email: ${email}</p><p>Phone: ${phone}</p><p>Message: ${message}</p>`,
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.log(error);
      res.status(500).send("An error occurred while sending the email.");
    } else {
      console.log("Email sent: " + info.response);
      res.status(200).send("Email sent: " + info.response);
    }
  });
});

// Check authentication status route
app.get("/check-auth", (req, res) => {
  if (req.session && req.session.userId) {
    res.status(200).json({
      authenticated: true,
      user: {
        id: req.session.userId,
        name: req.session.userName,
        email: req.session.userEmail,
      },
    });
  } else {
    res.status(200).json({ authenticated: false });
  }
});

// Serve static HTML files
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Start the server
app.listen(5000, () => {
  console.log("Server running on port 5000");
});

module.exports = con;
