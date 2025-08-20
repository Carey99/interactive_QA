import QAInterface from '@/components/QAInterface';

export default function Home() {
  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Matrix-style background pattern */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0 bg-gradient-to-br from-black via-green-950 to-black"></div>
      </div>
      
      <div className="container mx-auto px-4 py-8 relative z-10">
        <header className="text-center mb-8">
          <h1 className="text-5xl font-bold matrix-heading mb-4">
            <span className="text-green-400 font-mono tracking-wider">
              Q&A INTERFACE
            </span>
          </h1>
          <div className="matrix-text text-lg mb-2">
            <span className="text-green-300 font-mono">{'> '}</span>
            <span className="text-green-400">SYSTEM STATUS: ONLINE</span>
          </div>
          <p className="text-green-300 font-mono text-sm opacity-80">
            {'>'} Enter the Matrix... Ask any question about business startup
          </p>
        </header>
        <QAInterface />
      </div>
    </div>
  );
}
