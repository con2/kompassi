import { NextResponse, NextRequest } from "next/server";

export async function GET(_request: NextRequest) {
  return NextResponse.json({ status: "OK" }, { status: 200 });
}
