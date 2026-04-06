export const metadata = {
  title: 'AI App',
  description: 'My AI Project Deployment',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
