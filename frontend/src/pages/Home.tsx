import { Link } from 'react-router-dom';
import {
  CheckCircle,
  ArrowRight,
  Zap,
  Shield,
  BarChart3,
  Layout,
} from 'lucide-react';
import { Button } from '@/components/ui';
import { useAuthStore } from '@/store';

const features = [
  {
    icon: Layout,
    title: 'Intuitive Dashboard',
    description: 'Manage all your tasks in one place with a clean, modern interface.',
  },
  {
    icon: Zap,
    title: 'Fast & Responsive',
    description: 'Built with performance in mind. Lightning-fast interactions.',
  },
  {
    icon: Shield,
    title: 'Secure by Default',
    description: 'JWT authentication and secure API endpoints protect your data.',
  },
  {
    icon: BarChart3,
    title: 'Analytics & Insights',
    description: 'Track your productivity with detailed analytics and charts.',
  },
];

export function HomePage() {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-primary-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-accent-500/5 rounded-full blur-3xl" />
      </div>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32">
        <div className="text-center max-w-3xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-8 animate-fade-in">
            <CheckCircle className="w-4 h-4" />
            Open Source Task Management
          </div>

          {/* Heading */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white leading-tight animate-slide-up">
            Manage tasks with{' '}
            <span className="text-gradient">clarity</span>
          </h1>

          {/* Subheading */}
          <p className="text-xl text-gray-600 dark:text-gray-400 mt-6 animate-slide-up" style={{ animationDelay: '100ms' }}>
            TaskFlow is a modern, full-stack task management application
            built with FastAPI and React. Simple, fast, and beautiful.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-10 animate-slide-up" style={{ animationDelay: '200ms' }}>
            {isAuthenticated ? (
              <Link to="/dashboard">
                <Button size="lg">
                  Go to Dashboard
                  <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
            ) : (
              <>
                <Link to="/register">
                  <Button size="lg">
                    Get Started Free
                    <ArrowRight className="w-5 h-5" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="secondary" size="lg">
                    Sign In
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>

        {/* Dashboard Preview */}
        <div className="mt-20 relative animate-slide-up" style={{ animationDelay: '300ms' }}>
          <div className="absolute inset-0 bg-gradient-to-t from-gray-50 dark:from-gray-950 to-transparent z-10 h-32 bottom-0 top-auto" />
          <div className="card p-2 sm:p-4 shadow-2xl shadow-gray-200/50 dark:shadow-gray-900/50">
            <div className="aspect-[16/9] rounded-xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 overflow-hidden">
              {/* Mock dashboard preview */}
              <div className="p-6 space-y-4">
                <div className="h-8 w-48 bg-gray-300 dark:bg-gray-700 rounded-lg animate-shimmer" />
                <div className="grid grid-cols-4 gap-4">
                  {[1, 2, 3, 4].map((i) => (
                    <div
                      key={i}
                      className="h-24 bg-gray-300 dark:bg-gray-700 rounded-xl animate-shimmer"
                      style={{ animationDelay: `${i * 100}ms` }}
                    />
                  ))}
                </div>
                <div className="space-y-3">
                  {[1, 2, 3].map((i) => (
                    <div
                      key={i}
                      className="h-16 bg-gray-300 dark:bg-gray-700 rounded-xl animate-shimmer"
                      style={{ animationDelay: `${i * 100 + 400}ms` }}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-100 dark:bg-gray-900/50 py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
              Everything you need
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-4">
              A complete solution for personal and team task management
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="card p-6 hover:shadow-lg transition-shadow animate-fade-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="w-12 h-12 rounded-xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
              Built with modern tech
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-4">
              A portfolio-ready full-stack application using industry-standard tools
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-6">
            {['FastAPI', 'React', 'TypeScript', 'PostgreSQL', 'Tailwind CSS', 'Docker'].map(
              (tech) => (
                <div
                  key={tech}
                  className="px-6 py-3 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-medium"
                >
                  {tech}
                </div>
              )
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;

