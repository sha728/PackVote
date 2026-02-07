"use client";

import Link from "next/link";
import { Mail, Lock, User, ArrowRight } from "lucide-react";
import { useState } from "react";

export default function SignupPage() {
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
                <h1 className="text-3xl font-extrabold text-gray-900">Create an account</h1>
                <p className="text-gray-500 mt-2">Start planning your next adventure today.</p>
            </div>

            <button className="w-full flex items-center justify-center gap-3 bg-white border border-gray-200 text-gray-700 font-medium py-3 rounded-xl hover:bg-gray-50 transition mb-6">
                <img src="https://www.svgrepo.com/show/475656/google-color.svg" className="w-5 h-5" alt="Google" />
                Sign up with Google
            </button>

            <div className="relative flex items-center gap-4 py-4 mb-4">
                <div className="h-px bg-gray-200 flex-1" />
                <span className="text-xs text-gray-400 font-medium uppercase">Or sign up with email</span>
                <div className="h-px bg-gray-200 flex-1" />
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                    <div className="relative">
                        <User className="w-4 h-4 absolute left-3 top-3.5 text-gray-400" />
                        <input
                            type="text"
                            placeholder="John Doe"
                            className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition"
                            required
                        />
                    </div>
                </div>

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
                    <p className="text-xs text-gray-500 mt-1">Must be at least 8 characters</p>
                </div>

                <button
                    disabled={isLoading}
                    className="w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition flex items-center justify-center gap-2"
                >
                    {isLoading ? "Creating Account..." : <>Create Account <ArrowRight className="w-4 h-4" /></>}
                </button>
            </form>

            <p className="text-center text-sm text-gray-500 mt-8">
                Already have an account?{" "}
                <Link href="/login" className="font-semibold text-blue-600 hover:text-blue-500">
                    Sign in
                </Link>
            </p>
        </div>
    );
}
