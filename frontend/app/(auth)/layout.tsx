export default function AuthLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen grid lg:grid-cols-2">
            {/* Left: Content */}
            <div className="flex items-center justify-center p-8 bg-white">
                <div className="w-full max-w-md space-y-8 animate-in slide-in-from-left-5 fade-in duration-500">
                    {children}
                </div>
            </div>

            {/* Right: Creative Visual */}
            <div className="hidden lg:flex flex-col justify-between p-12 bg-gradient-to-br from-blue-600 to-indigo-900 text-white relative overflow-hidden">
                {/* Abstract Shapes */}
                <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-pink-500/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />

                <div className="relative z-10">
                    <h2 className="text-3xl font-bold mb-2">PackVote ✈️</h2>
                    <p className="text-blue-100">Plan trips without the drama.</p>
                </div>

                <div className="relative z-10 space-y-6">
                    <blockquote className="text-2xl font-medium leading-relaxed">
                        "Finally, a way to get my friends to actually agree on a destination. The AI itinerary saved us hours of planning."
                    </blockquote>
                    <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center font-bold">JD</div>
                        <div>
                            <div className="font-semibold">John Doe</div>
                            <div className="text-sm text-blue-200">Trip to Goa</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
