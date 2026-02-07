"use client";

import Link from "next/link";
import { Mail, Lock, ArrowRight } from "lucide-react";
import { useState } from "react";

export default function LoginPage() {
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        // Simulate API call
        setTimeout(() => setIsLoading(false), 2000);
    };

    return (
        <div>
            <div className="mb-8">
                <h1 className="text-3xl font-extrabold text-gray-900">Welcome back</h1>
                <p className="text-gray-500 mt-2">Enter your details to access your trips.</p>
            </div>

            {/* Google Button */}
            <button className="w-full flex items-center justify-center gap-3 bg-white border border-gray-200 text-gray-700 font-medium py-3 rounded-xl hover:bg-gray-50 transition mb-6">
                <img src="https://www.svgrepo.com/show/475656/google-color.svg" className="w-5 h-5" alt="Google" />
                Continue with Google
            </button>

            <div className="relative flex items-center gap-4 py-4 mb-4">
                <div className="h-px bg-gray-200 flex-1" />
                <span className="text-xs text-gray-400 font-medium uppercase">Or continue with email</span>
                <div className="h-px bg-gray-200 flex-1" />
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <div className="relative">
                        <Mail className="w-4 h-4 absolute left-3 top-3.5 text-gray-400" />
                        <input
                            type="email"
                            placeholder="you@example.com"
                            className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                            required
                        />
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                    <div className="relative">
                        <Lock className="w-4 h-4 absolute left-3 top-3.5 text-gray-400" />
                        <input
                            type="password"
                            placeholder="••••••••"
                            className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                            required
                        />
                    </div>
                </div>

                <button
                    disabled={isLoading}
                    className="w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition flex items-center justify-center gap-2"
                >
                    {isLoading ? "Signing in..." : <>Sign In <ArrowRight className="w-4 h-4" /></>}
                </button>
            </form>

            <p className="text-center text-sm text-gray-500 mt-8">
                Don't have an account?{" "}
                <Link href="/signup" className="font-semibold text-blue-600 hover:text-blue-500">
                    Sign up for free
                </Link>
            </p>
        </div>
    );
}
