import { MainNav } from '@/components/navigation/main-nav';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen ">
      <MainNav />
      <main className="container mx-auto py-6 px-4">
        {children}
      </main>
    </div>
  );
}