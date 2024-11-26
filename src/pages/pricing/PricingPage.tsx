import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle2 } from 'lucide-react';

type BillingPeriod = 'monthly' | 'quarterly' | 'yearly';

type Feature = {
  searches: number;
  period: string;
  brands: number;
  type: string;
};

type PricingPlan = {
  name: string;
  description: string;
  basePrice: number;
  features: Feature[];
  color: string;
  popular?: boolean;
};

const PricingPage = () => {
  const [billingPeriod, setBillingPeriod] = useState<BillingPeriod>('monthly');

  const calculatePrice = (basePrice: number, period: BillingPeriod): number => {
    switch (period) {
      case 'quarterly':
        return Number((basePrice * 0.85 * 3).toFixed(0));
      case 'yearly':
        return Number((basePrice * 0.75 * 12).toFixed(0));
      default:
        return basePrice;
    }
  };

  const calculateMonthlyPrice = (totalPrice: number, period: BillingPeriod): number => {
    switch (period) {
      case 'quarterly':
        return Number((totalPrice / 3).toFixed(0));
      case 'yearly':
        return Number((totalPrice / 12).toFixed(0));
      default:
        return totalPrice;
    }
  };

  const plans: PricingPlan[] = [
    {
      name: 'Starter',
      description: 'Perfect for brands with smaller needs.',
      basePrice: 99,
      features: [
        { searches: 20, period: '/month', brands: 200, type: 'in lists' },
        { searches: 20, period: '/month', brands: 500, type: 'in CRM' }
      ],
      color: 'bg-[#F4A261]'
    },
    {
      name: 'Pro',
      description: 'Ideal for companies working with brands on a regular basis.',
      basePrice: 169,
      features: [
        { searches: 50, period: '/month', brands: 2000, type: 'in lists' },
        { searches: 50, period: '/month', brands: 5000, type: 'in CRM' }
      ],
      color: 'bg-[#E76F51]',
      popular: true
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col items-center mb-8">
        <div className="inline-flex rounded-md shadow-sm" role="group">
          {(['monthly', 'quarterly', 'yearly'] as const).map((period) => (
            <Button
              key={period}
              variant={billingPeriod === period ? 'default' : 'outline'}
              onClick={() => setBillingPeriod(period)}
              className="capitalize"
            >
              {period}
            </Button>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {plans.map((plan) => {
          const totalPrice = calculatePrice(plan.basePrice, billingPeriod);
          const monthlyPrice = calculateMonthlyPrice(totalPrice, billingPeriod);

          return (
            <Card key={plan.name} className={`relative ${plan.popular ? 'border-primary' : ''}`}>
              {plan.popular && (
                <div className="absolute -top-3 right-4 bg-primary text-white px-3 py-1 rounded-full text-sm">
                  Popular
                </div>
              )}
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className={`w-8 h-8 rounded-full ${plan.color}`} />
                  {plan.name}
                </CardTitle>
                <p className="text-muted-foreground">{plan.description}</p>
              </CardHeader>
              <CardContent>
                <div className="mb-4">
                  <p className="text-3xl font-bold">${totalPrice}</p>
                  {billingPeriod !== 'monthly' && (
                    <p className="text-sm text-muted-foreground">
                      ${monthlyPrice}/month
                    </p>
                  )}
                </div>
                <ul className="space-y-2">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-center gap-2">
                      <CheckCircle2 className="w-5 h-5 text-green-500" />
                      <span>
                        {feature.searches} searches{feature.period}, {feature.brands} brands {feature.type}
                      </span>
                    </li>
                  ))}
                </ul>
                <Button className="w-full mt-6">Get Started</Button>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default PricingPage;