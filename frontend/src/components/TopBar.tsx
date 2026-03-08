interface Props {
  onUpload: (files: FileList | null) => void;
  onGenerate: (prompt: string, size: "1024x1024" | "1024x1536" | "1536x1024", provider: string) => void;
  generating: boolean;
}

export default function TopBar({ onUpload, onGenerate, generating }: Props) {
  return (
    <header className="topbar">
      <div>
        <h1>AI Photo Studio</h1>
        <p>Local-first gallery, editing, and AI image generation.</p>
      </div>
      <div className="top-actions">
        <label className="button-like">
          Upload Images
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp"
            multiple
            onChange={(e) => onUpload(e.target.files)}
            hidden
          />
        </label>
        <form
          className="generate-form"
          onSubmit={(e) => {
            e.preventDefault();
            const data = new FormData(e.currentTarget);
            const prompt = String(data.get("prompt") || "").trim();
            const size = String(data.get("size") || "1024x1024").trim() as
              | "1024x1024"
              | "1024x1536"
              | "1536x1024";
            const provider = String(data.get("provider") || "").trim();
            if (!prompt) return;
            onGenerate(prompt, size, provider);
            e.currentTarget.reset();
          }}
        >
          <input name="prompt" placeholder="Generate with prompt" aria-label="Prompt" />
          <select name="size" defaultValue="1024x1024" aria-label="Size">
            <option value="1024x1024">1024x1024</option>
            <option value="1024x1536">1024x1536</option>
            <option value="1536x1024">1536x1024</option>
          </select>
          <select name="provider" defaultValue="">
            <option value="">Env default</option>
            <option value="nano-banana">nano-banana</option>
            <option value="gpt-image">gpt-image</option>
            <option value="mock">mock</option>
          </select>
          <button type="submit" disabled={generating}>{generating ? "Generating..." : "Generate"}</button>
        </form>
      </div>
    </header>
  );
}
