"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { Users, MapPin, Calendar, DollarSign } from "lucide-react";

export default function CreateGroup() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        name: "",
        creator_email: "",
        start_city: "",
        max_budget: 10000,
        travel_month: "May",
        duration: 3,
        group_size: 4,
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await axios.post("http://localhost:8000/api/v1/groups", formData);
            router.push(`/group/${res.data.id}`);
        } catch (error) {
            console.error("Failed to create group", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Start a Trip 🌍</h1>
                    <p className="text-gray-500">Create a voting room for your squad</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Group Name</label>
                        <div className="relative">
                            <Users className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
                            <input
                                type="text"
                                required
                                placeholder="e.g. Goa 2026"
                                className="w-full pl-10 pr-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Creator Email</label>
                        <div className="relative">
                            <Users className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
                            <input
                                type="email"
                                required
                                placeholder="your@email.com"
                                className="w-full pl-10 pr-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                                value={formData.creator_email}
                                onChange={(e) => setFormData({ ...formData, creator_email: e.target.value })}
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Start City</label>
                            <div className="relative">
                                <MapPin className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
                                <input
                                    type="text"
                                    required
                                    placeholder="e.g. Mumbai"
                                    className="w-full pl-10 pr-4 py-2 border rounded-xl"
                                    value={formData.start_city}
                                    onChange={(e) => setFormData({ ...formData, start_city: e.target.value })}
                                />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Month</label>
                            <div className="relative">
                                <Calendar className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
                                <select
                                    className="w-full pl-10 pr-4 py-2 border rounded-xl bg-white"
                                    value={formData.travel_month}
                                    onChange={(e) => setFormData({ ...formData, travel_month: e.target.value })}
                                >
                                    {["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].map(m => (
                                        <option key={m} value={m}>{m}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Max Budget (Per Person)</label>
                        <div className="relative">
                            <DollarSign className="absolute left-3 top-3 text-gray-400 w-5 h-5" />
                            <input
                                type="number"
                                required
                                min="1000"
                                step="500"
                                className="w-full pl-10 pr-4 py-2 border rounded-xl"
                                value={formData.max_budget}
                                onChange={(e) => setFormData({ ...formData, max_budget: Number(e.target.value) })}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition transform active:scale-95 disabled:opacity-50"
                    >
                        {loading ? "Creating..." : "Create Voting Room →"}
                    </button>
                </form>
            </div>
        </div>
    );
}
