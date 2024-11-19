import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv'; // Ensure dotenv is imported correctly

const app = express();
app.use(cors());
app.use(express.json());
dotenv.config(); // Loads environment variables from the .env file

app.listen(process.env.PORT, () => {
    console.log(`Server is Running on Port ${process.env.PORT}`); // Corrected string interpolation
});
