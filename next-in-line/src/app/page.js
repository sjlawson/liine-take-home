'use client';

import Image from "next/image";
import { useState, useEffect } from 'react';
import { Button, Typography } from '@mui/material';
import moment from 'moment';


const datetimeStyle = {
  color: "black"
};

const getRestaurants = (datetime) => {

};

export default function Home() {
  const [data, setData] = useState(null);
  const [isLoading, setLoading] = useState(true);
  const [dateTimeValue, setDateTimeValue] = useState(moment().format('YYYY-MM-DDTHH:mm'));

  const handleChange = (event) => {
    setDateTimeValue(event.target.value);
  };

  const handleDateSubmit = () => {
    // Convert the string value to a Date object if needed:
    setLoading(true);
    const dateObj = new Date(dateTimeValue);
    console.log(dateObj);
    fetch('/api/hours?datetime=' + dateTimeValue)
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetch('/api/hours?datetime=' + dateTimeValue)
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      });
  }, []);

  return (
      <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">

      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div>
        <Image
          className="dark:invert"
          src="/coherent_auto_logo.svg"
          alt="Coherent Automation logo"
          width={180}
          height={38}
          priority
        />
        <Typography variant="h2">
          Coherent Automation
        </Typography>
        </div>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <div>
            Pick a date and time to see what's open!
          </div>
          <div style={datetimeStyle}>
            <input
              aria-label="Date and time"
              type="datetime-local"
              value={dateTimeValue}
              onChange={handleChange}
            />
          </div>
          <div>
            <Button variant="contained" onClick={handleDateSubmit} >Find some cooks!</Button>
          </div>

      </div>

      <ul className="list-inside list-decimal text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
        {data && data.map((r_data) => (
          <li key={r_data.restaurant} className="mb-2">{r_data.restaurant}</li>
        ))}
      </ul>

    </main>
    <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">

    </footer>
    </div>
  );
}
