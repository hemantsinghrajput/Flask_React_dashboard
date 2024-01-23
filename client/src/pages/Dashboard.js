import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard({ location }) {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log('Fetching dashboard data...');
                const response = await axios.get(`http://127.0.0.1:5000/dashboard`, {
                    withCredentials: true,
                });

                console.log('Dashboard data received:', response.data);
                setUserData(response.data);
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
                // Handle errors as needed
            }
        };

        fetchData();
    }, []);


    return (
        <div>
            <h2>Dashboard</h2>
            {userData ? (
                <div>
                    <p>Welcome, {userData.name}!</p>
                    <p>Email: {userData.email}</p>
                    {/* Add other dashboard information here */}
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}
