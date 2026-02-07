"use client";

import Link from "next/link";
import { Users, MapPin, Calendar, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex flex-col items-center justify-center p-8 text-center font-sans">
      <div className="max-w-4xl mx-auto space-y-8">

        {/* Hero Section */}
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-5 duration-700">
          <h1 className="text-6xl font-extrabold text-gray-900 tracking-tight">
            Plan Trips without the <span className="text-blue-600">Drama</span> ✈️
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Stop fighting over WhatsApp. Collect preferences, vote on destinations, and get an AI-generated itinerary that keeps everyone happy.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8">
          <Link href="/group/new" className="group relative inline-flex h-12 items-center justify-center overflow-hidden rounded-full bg-blue-600 px-8 font-medium text-white transition-all duration-300 hover:bg-blue-700 hover:w-56 w-48 shadow-lg hover:shadow-xl">
            <span className="mr-2">Start a Trip</span>
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </Link>
          <button disabled className="px-8 py-3 rounded-full border border-gray-300 text-gray-400 cursor-not-allowed bg-white/50">
            Join Existing (Enter ID)
          </button>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 text-left">
          <FeatureCard
            icon={<Users className="w-6 h-6 text-purple-600" />}
            title="Invite Squad"
            desc="Add friends via email. We chase them to fill out the survey."
          />
          <FeatureCard
            icon={<MapPin className="w-6 h-6 text-pink-600" />}
            title="Smart Ranking"
            desc="We rank places based on everyone's budget, weather, and vibe."
          />
          <FeatureCard
            icon={<Calendar className="w-6 h-6 text-green-600" />}
            title="AI Itinerary"
            desc="Get a day-wise plan tailored to your group's constraints."
          />
        </div>

      </div>
    </div>
  );
}

function FeatureCard({ icon, title, desc }: { icon: any, title: string, desc: string }) {
  return (
    <div className="bg-white/80 backdrop-blur-sm p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition">
      <div className="bg-gray-50 w-12 h-12 rounded-xl flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="font-bold text-gray-900 text-lg mb-2">{title}</h3>
      <p className="text-gray-500 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}
