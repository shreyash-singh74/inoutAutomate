import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/Input";
import { FormProvider, useForm } from "react-hook-form";
import { LoginSchema, LoginType, OtpSchema, OtpType } from "@/lib/schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form } from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { Link } from "@tanstack/react-router";
import { toast } from "sonner";

const SignInForm = () => {
  const [pending, setPending] = useState(false);
  const [otpSent, setOtpSent] = useState(false);
  const [email, setEmail] = useState("");

  const form = useForm<LoginType>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: "",
    },
  });

  const otpForm = useForm<OtpType>({
    resolver: zodResolver(OtpSchema),
    defaultValues: {
      otp: "",
    },
  });

  const onSubmit = async (values: LoginType) => {
    setPending(true);
    setEmail(values.email);
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    });
    if (res.status !== 200) {
      toast.error("Failed to send OTP");
      setPending(false);
      return;
    }
    toast.success("OTP sent to your email");
    setOtpSent(true);
    setPending(false);
  };

  const onOtpSubmit = async (values: OtpType) => {
    setPending(true);
    const res = await fetch("/api/auth/verify-login-otp", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        email: email,
        otp: values.otp,
      }),
    });
    if (res.status !== 200) {
      toast.error("Invalid OTP");
      setPending(false);
      return;
    }
    toast.success("Login successful");
    setPending(false);
    window.location.href = "/";
  };

  return (
    <Card className="w-[90%] md:w-[50%] lg:w-[40%] m-auto">
      <CardHeader>
        <h1 className="text-3xl font-bold m-auto">SignIn</h1>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form className="w-full space-y-4" onSubmit={form.handleSubmit(onSubmit)}>
            <FormProvider {...form}>
              <Input label="Email" name="email" />
            </FormProvider>
            <Button className="bg-[#d17a00] w-full text-white text-[16px]" disabled={pending}>
              {pending ? "pending..." : "Send OTP"}
            </Button>
          </form>
        </Form>
        {otpSent && (
          <Form {...otpForm}>
            <form className="w-full space-y-4" onSubmit={otpForm.handleSubmit(onOtpSubmit)}>
              <FormProvider {...otpForm}>
                <Input label="OTP" name="otp" />
              </FormProvider>
              <Button className="bg-[#d17a00] w-full text-white text-[16px]" disabled={pending}>
                {pending ? "pending..." : "Verify OTP"}
              </Button>
            </form>
          </Form>
        )}
      </CardContent>
      <CardFooter className="flex flex-col gap-3 w-full">
        <Link className="border-[#d17a00] border-2 hover:border-[#d17a00] text-black text-[16px] rounded-lg py-1 text-center w-full" to="/signup">
          SignUp
        </Link>
      </CardFooter>
    </Card>
  );
};

export default SignInForm;
