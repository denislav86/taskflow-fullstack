import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { CheckCircle, Mail, Lock, User } from 'lucide-react';
import { Button, Input } from '@/components/ui';
import { useRegister } from '@/hooks';
import type { RegisterData } from '@/types';

interface FormData extends RegisterData {
  confirmPassword: string;
}

export function RegisterPage() {
  const registerUser = useRegister();
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<FormData>();

  const password = watch('password');

  const onSubmit = (data: FormData) => {
    registerUser.mutate({
      email: data.email,
      password: data.password,
      full_name: data.full_name,
    });
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
      {/* Background decoration */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl" />
      </div>

      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center p-3 rounded-2xl bg-primary-600 mb-4">
            <CheckCircle className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Create your account
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Get started with TaskFlow today
          </p>
        </div>

        {/* Form */}
        <div className="card p-6 sm:p-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <div className="relative">
              <User className="absolute left-3 top-9 w-5 h-5 text-gray-400" />
              <Input
                label="Full Name"
                type="text"
                placeholder="John Doe"
                className="pl-10"
                error={errors.full_name?.message}
                {...register('full_name')}
              />
            </div>

            <div className="relative">
              <Mail className="absolute left-3 top-9 w-5 h-5 text-gray-400" />
              <Input
                label="Email"
                type="email"
                placeholder="you@example.com"
                className="pl-10"
                error={errors.email?.message}
                {...register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address',
                  },
                })}
              />
            </div>

            <div className="relative">
              <Lock className="absolute left-3 top-9 w-5 h-5 text-gray-400" />
              <Input
                label="Password"
                type="password"
                placeholder="••••••••"
                className="pl-10"
                error={errors.password?.message}
                {...register('password', {
                  required: 'Password is required',
                  minLength: {
                    value: 8,
                    message: 'Password must be at least 8 characters',
                  },
                })}
              />
            </div>

            <div className="relative">
              <Lock className="absolute left-3 top-9 w-5 h-5 text-gray-400" />
              <Input
                label="Confirm Password"
                type="password"
                placeholder="••••••••"
                className="pl-10"
                error={errors.confirmPassword?.message}
                {...register('confirmPassword', {
                  required: 'Please confirm your password',
                  validate: (value) =>
                    value === password || 'Passwords do not match',
                })}
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              isLoading={registerUser.isPending}
            >
              Create Account
            </Button>
          </form>
        </div>

        {/* Login link */}
        <p className="text-center mt-6 text-gray-600 dark:text-gray-400">
          Already have an account?{' '}
          <Link
            to="/login"
            className="font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;

