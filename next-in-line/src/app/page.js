'use client'

import Image from "next/image";
import { useState, useEffect } from 'react'


export default function Home() {
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/hours?datetime=2024-10-22T13:36')
      .then((res) => res.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
  }, [])

  console.log(data);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <Image
          className="dark:invert"
          src="/coherent_auto_logo.svg"
          alt="Coherent Automation logo"
          width={180}
          height={38}
          priority
      />

        <ul className="list-inside list-decimal text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
      {data && data.map((r_data) => (
          <li key={r_data.restaurant} className="mb-2">{r_data.restaurant}</li>
          ))}
        </ul>

      <div className="flex gap-4 items-center flex-col sm:flex-row">

      </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>
      </footer>
    </div>
  );
}
