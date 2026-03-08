import type { ImageAsset, SortKey, SortOrder } from "../types";

const toQuery = (params: Record<string, string | number | undefined>) => {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== "") {
      query.set(k, String(v));
    }
  });
  return query.toString();
};

export async function listImages(search: string, sort: SortKey, order: SortOrder): Promise<ImageAsset[]> {
  const query = toQuery({ search, sort, order });
  const resp = await fetch(`/api/images?${query}`);
  if (!resp.ok) throw new Error("Failed to load images");
  const data = (await resp.json()) as { items: ImageAsset[] };
  return data.items;
}

export async function uploadImage(file: File): Promise<ImageAsset> {
  const formData = new FormData();
  formData.append("file", file);
  const resp = await fetch("/api/images/upload", { method: "POST", body: formData });
  if (!resp.ok) throw new Error("Upload failed");
  return (await resp.json()) as ImageAsset;
}

export async function generateImage(payload: {
  prompt: string;
  size: "1024x1024" | "1024x1536" | "1536x1024";
  style?: string;
  provider?: string;
}): Promise<ImageAsset> {
  const resp = await fetch("/api/ai/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!resp.ok) throw new Error("Generation failed");
  const data = (await resp.json()) as { image: ImageAsset };
  return data.image;
}
