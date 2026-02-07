"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import axios from "axios";
import { UserPlus, RefreshCw, CheckCircle, Clock } from "lucide-react";

interface Participant {
    id: string;
    name: string;
    status: string;
    survey_link: string;
}

interface Place {
    name: string;
    state: string;
    description: string;
    match_score?: number;
    weather_summary?: any;
}

export default function GroupDashboard() {
    const params = useParams();
    const groupId = params.id;

    const [group, setGroup] = useState<any>(null);
    const [participants, setParticipants] = useState<Participant[]>([]);
    const [recommendations, setRecommendations] = useState<Place[]>([]);

    const [newMember, setNewMember] = useState({ name: "", email: "" });
    const [loadingRecs, setLoadingRecs] = useState(false);

    const [selectedPlace, setSelectedPlace] = useState<Place | null>(null);
    const [itinerary, setItinerary] = useState<any>(null);
    const [loadingPlan, setLoadingPlan] = useState(false);

    useEffect(() => {
        if (groupId) {
            fetchGroupData();
        }
    }, [groupId]);

    const fetchGroupData = async () => {
        try {
            const res = await axios.get(`http://127.0.0.1:8000/api/v1/groups/${groupId}`);
            setGroup(res.data);
            setParticipants(res.data.participants || []);
        } catch (e) {
            console.error(e);
        }
    };

    const addMember = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post(`http://127.0.0.1:8000/api/v1/groups/${groupId}/participants`, newMember);
            setNewMember({ name: "", email: "" });
            fetchGroupData(); // Refresh list
        } catch (e: any) {
            console.error(e);
            const msg = e.response?.data?.detail || e.message || "Failed to add member";
            alert(`Error: ${msg}`);
        }
    };

    const syncAndRecommend = async () => {
        setLoadingRecs(true);
        try {
            // 1. Trigger Sync
            await axios.post(`http://127.0.0.1:8000/api/v1/sync/${groupId}`);
            // 2. Get Recs
            const res = await axios.post(`http://127.0.0.1:8000/api/v1/groups/${groupId}/recommendations`);
            setRecommendations(res.data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoadingRecs(false);
        }
    };

    const generatePlan = async (place: Place) => {
        setSelectedPlace(place);
        setLoadingPlan(true);
        setItinerary(null);
        try {
            const res = await axios.post(`http://127.0.0.1:8000/api/v1/groups/${groupId}/itinerary`, {
                destination: place.name,
                weather_summary: JSON.stringify(place.weather_summary || {})
            });
            setItinerary(res.data);
        } catch (e) {
            console.error(e);
            alert("Failed to generate plan");
        } finally {
            setLoadingPlan(false);
        }
    };

    if (!group) return <div className="p-10 text-center">Loading Room...</div>;

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <header className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">{group.name}</h1>
                        <p className="text-gray-500">Budget: ₹{group.max_budget} • {group.start_city}</p>
                    </div>
                    <div className="flex gap-2">
                        <button
                            onClick={syncAndRecommend}
                            className="bg-indigo-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-indigo-700 transition"
                        >
                            <RefreshCw className={`w-4 h-4 ${loadingRecs ? "animate-spin" : ""}`} />
                            Sync & Rank
                        </button>
                    </div>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Left: Participants */}
                    <div className="bg-white p-6 rounded-2xl shadow-sm h-fit">
                        <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <UsersCount count={participants.length} /> Squad
                        </h2>

                        <div className="space-y-3 mb-6">
                            {participants.map((p) => (
                                <div key={p.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                                    <div>
                                        <div className="font-medium">{p.name}</div>
                                        <div className="text-xs text-gray-400">
                                            {/* @ts-ignore - MVP check for invite_status in p or fallback */}
                                            {p.invite_status ? `Invite: ${p.invite_status}` : "Invited via Twilio"}
                                        </div>
                                    </div>
                                    {p.status === "completed" ? (
                                        <CheckCircle className="w-5 h-5 text-green-500" />
                                    ) : (
                                        <Clock className="w-5 h-5 text-orange-400" />
                                    )}
                                </div>
                            ))}
                        </div>

                        <form onSubmit={addMember} className="border-t pt-4">
                            <h3 className="text-sm font-semibold mb-3">Invite Friend</h3>
                            <input
                                className="w-full mb-2 p-2 border rounded-lg text-sm"
                                placeholder="Name"
                                value={newMember.name}
                                onChange={e => setNewMember({ ...newMember, name: e.target.value })}
                                required
                            />
                            <input
                                className="w-full mb-3 p-2 border rounded-lg text-sm"
                                placeholder="Email (friend@example.com)"
                                type="email"
                                value={newMember.email}
                                onChange={e => setNewMember({ ...newMember, email: e.target.value })}
                                required
                            />
                            <button className="w-full bg-gray-900 text-white py-2 rounded-lg text-sm flex items-center justify-center gap-2">
                                <UserPlus className="w-4 h-4" /> Send Invite
                            </button>
                        </form>
                    </div>

                    {/* Right: Results */}
                    <div className="lg:col-span-2">
                        <h2 className="text-lg font-bold mb-4">🏆 Top Recommendations</h2>

                        {recommendations.length === 0 ? (
                            <div className="bg-white p-10 rounded-2xl shadow-sm text-center text-gray-400">
                                <p>Waiting for votes...</p>
                                <p className="text-sm">Add participants and click "Sync & Rank" to see magic.</p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {recommendations.map((place, idx) => (
                                    <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-4">
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <div className="flex items-center gap-3 mb-1">
                                                    <h3 className="text-xl font-bold text-gray-900">{place.name}</h3>
                                                    <span className="bg-green-100 text-green-800 text-xs px-2 py-0.5 rounded-full font-bold">
                                                        Match: {place.match_score}%
                                                    </span>
                                                </div>
                                                <p className="text-gray-500 text-sm line-clamp-2">{place.description}</p>
                                            </div>
                                            <button
                                                onClick={() => generatePlan(place)}
                                                className="bg-gray-900 text-white px-3 py-1 rounded-lg text-sm hover:bg-black transition"
                                            >
                                                Generate Itinerary ✨
                                            </button>
                                        </div>

                                        {/* Inline Itinerary View if Selected */}
                                        {selectedPlace?.name === place.name && (
                                            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 mt-2">
                                                {loadingPlan ? (
                                                    <div className="flex items-center gap-2 text-gray-500">
                                                        <Clock className="w-4 h-4 animate-spin" />
                                                        Generating AI Plan...
                                                    </div>
                                                ) : itinerary ? (
                                                    <div>
                                                        <h4 className="font-bold text-lg mb-2">{itinerary.title}</h4>
                                                        <p className="text-sm text-gray-600 mb-4">{itinerary.summary}</p>
                                                        <div className="space-y-3">
                                                            {itinerary.daily_plan?.map((day: any, i: number) => (
                                                                <div key={i} className="text-sm">
                                                                    <span className="font-bold">Day {day.day}:</span> {day.activities}
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>
                                                ) : null}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function UsersCount({ count }: { count: number }) {
    return <span className="bg-gray-100 text-gray-600 px-2 py-0.5 rounded text-xs">{count}</span>;
}
