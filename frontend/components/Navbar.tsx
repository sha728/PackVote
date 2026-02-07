"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Plane, Menu, X } from "lucide-react";
import { useState } from "react";

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const pathname = usePathname();

    const isAuthPage = pathname.includes("/login") || pathname.includes("/signup");

    if (isAuthPage) return null; // Don't show generic navbar on auth pages

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-lg border-b border-white/20 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2 group">
                        <div className="bg-blue-600 p-2 rounded-lg group-hover:rotate-12 transition-transform">
                            <Plane className="w-5 h-5 text-white" />
                        </div>
                        <span className="font-bold text-xl tracking-tight text-gray-900">
                            Pack<span className="text-blue-600">Vote</span>
                        </span>
                    </Link>

                    {/* Desktop Nav */}
                    <div className="hidden md:flex items-center gap-8">
                        <NavLink href="/features">Features</NavLink>
                        <NavLink href="/how-it-works">How it Works</NavLink>
                        <NavLink href="/about">About Us</NavLink>

                        <div className="flex items-center gap-4 ml-4">
                            <Link href="/login" className="text-sm font-semibold text-gray-700 hover:text-blue-600 transition">
                                Log in
                            </Link>
                            <Link href="/signup" className="px-5 py-2.5 rounded-full bg-gray-900 text-white text-sm font-medium hover:bg-gray-800 transition shadow-lg shadow-gray-200">
                                Sign up
                            </Link>
                        </div>
                    </div>

                    {/* Mobile Menu Button */}
                    <button onClick={() => setIsOpen(!isOpen)} className="md:hidden p-2 text-gray-600">
                        {isOpen ? <X /> : <Menu />}
                    </button>
                </div>
            </div>

            {/* Mobile Nav */}
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="md:hidden absolute top-16 left-0 right-0 bg-white border-b border-gray-100 p-4 shadow-xl"
                >
                    <div className="flex flex-col gap-4">
                        <Link href="/features" className="text-gray-600 py-2">Features</Link>
                        <Link href="/login" className="text-gray-600 py-2">Log in</Link>
                        <Link href="/signup" className="bg-blue-600 text-white py-3 rounded-xl text-center font-bold">
                            Sign up Free
                        </Link>
                    </div>
                </motion.div>
            )}
        </nav>
    );
}

function NavLink({ href, children }: { href: string, children: React.ReactNode }) {
    return (
        <Link href={href} className="text-sm font-medium text-gray-500 hover:text-gray-900 transition relative group">
            {children}
            <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-blue-600 transition-all group-hover:w-full" />
        </Link>
    );
}
