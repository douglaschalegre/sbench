import * as React from 'react'
import * as ProgressPrimitive from '@radix-ui/react-progress'
import * as RadioGroupPrimitive from '@radix-ui/react-radio-group'
import { cn } from '../lib/utils'

export const Button = React.forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'outline' | 'ghost' | 'danger' }>(
  ({ className, variant = 'primary', ...props }, ref) => (
    <button ref={ref} className={cn(
      'inline-flex h-11 items-center justify-center gap-2 rounded-xl px-5 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-forest focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-45',
      variant === 'primary' && 'bg-forest text-white hover:bg-[#103a2c]',
      variant === 'outline' && 'border border-line bg-paper text-ink hover:border-moss hover:bg-white',
      variant === 'ghost' && 'text-ink hover:bg-black/5',
      variant === 'danger' && 'bg-red-700 text-white hover:bg-red-800', className,
    )} {...props} />
  ),
)
Button.displayName = 'Button'

export function Progress({ value, className }: { value: number; className?: string }) {
  return <ProgressPrimitive.Root className={cn('relative h-1.5 overflow-hidden rounded-full bg-black/10', className)} value={value}>
    <ProgressPrimitive.Indicator className="h-full bg-amber transition-transform duration-500" style={{ transform: `translateX(-${100 - value}%)` }} />
  </ProgressPrimitive.Root>
}

export function Segmented({ value, onValueChange, options, ariaLabel }: { value?: string; onValueChange: (value: string) => void; options: { value: string; label: string }[]; ariaLabel: string }) {
  return <RadioGroupPrimitive.Root value={value} onValueChange={onValueChange} aria-label={ariaLabel} className="grid grid-cols-3 gap-2 sm:grid-cols-4">
    {options.map((option) => <label key={option.value} className={cn('cursor-pointer rounded-xl border px-3 py-2.5 text-center text-sm font-medium transition', value === option.value ? 'border-forest bg-forest text-white' : 'border-line bg-white hover:border-moss')}>
      <RadioGroupPrimitive.Item value={option.value} className="sr-only" />{option.label}
    </label>)}
  </RadioGroupPrimitive.Root>
}

export function Scale({ value, onChange, low, high }: { value?: number; onChange: (value: number) => void; low: string; high: string }) {
  return <div>
    <div className="grid grid-cols-5 gap-2">
      {[1, 2, 3, 4, 5].map((number) => <button type="button" key={number} onClick={() => onChange(number)} className={cn('aspect-square max-h-11 rounded-xl border text-sm font-semibold transition', value === number ? 'border-forest bg-forest text-white' : 'border-line bg-white hover:border-moss')}>{number}</button>)}
    </div>
    <div className="mt-1.5 flex justify-between text-[11px] text-black/45"><span>{low}</span><span>{high}</span></div>
  </div>
}

export function FieldLabel({ children, optional }: { children: React.ReactNode; optional?: boolean }) {
  return <div className="mb-2 flex items-center justify-between text-sm font-semibold text-ink"><span>{children}</span>{optional && <span className="text-[11px] font-normal uppercase tracking-wider text-black/40">opcional</span>}</div>
}
