import { useCallback, useEffect, useMemo, useState } from "react";

import { generateImage, listImages, uploadImage } from "./api/client";
import EditorPanel from "./components/EditorPanel";
import GalleryPanel from "./components/GalleryPanel";
import TopBar from "./components/TopBar";
import type { ImageAsset, SortKey, SortOrder } from "./types";

export default function App() {
  const [items, setItems] = useState<ImageAsset[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<SortKey>("created_at");
  const [order, setOrder] = useState<SortOrder>("desc");
  const [loading, setLoading] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selected = useMemo(() => items.find((i) => i.id === selectedId) ?? null, [items, selectedId]);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listImages(search, sort, order);
      setItems(data);
      if (data.length && !selectedId) setSelectedId(data[0].id);
      if (selectedId && !data.some((it) => it.id === selectedId)) setSelectedId(data[0]?.id ?? null);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, [order, search, selectedId, sort]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const onUpload = async (fileList: FileList | null) => {
    if (!fileList?.length) return;
    setBusy(true);
    try {
      for (const file of Array.from(fileList)) {
        await uploadImage(file);
      }
      await refresh();
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  const onGenerate = async (
    prompt: string,
    size: "1024x1024" | "1024x1536" | "1536x1024",
    provider: string,
  ) => {
    setBusy(true);
    try {
      const created = await generateImage({ prompt, size, provider: provider || undefined });
      await refresh();
      setSelectedId(created.id);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="app-shell">
      <TopBar onUpload={onUpload} onGenerate={onGenerate} generating={busy} />
      {error ? <p className="error-banner">{error}</p> : null}
      <main className="workspace">
        <GalleryPanel
          items={items}
          selectedId={selectedId}
          search={search}
          sort={sort}
          order={order}
          loading={loading}
          onSearch={setSearch}
          onSort={setSort}
          onOrder={setOrder}
          onSelect={(img) => setSelectedId(img.id)}
        />
        <EditorPanel selected={selected} />
      </main>
    </div>
  );
}
