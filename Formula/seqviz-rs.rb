class SeqvizRs < Formula
  desc "Terminal browser for biological sequences and alignment records"
  homepage "https://github.com/Georicl/seqviz-rs"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.0/seqviz-rs-aarch64-apple-darwin.tar.gz"
      sha256 "76bb4b624653a1bf51eafd959d75a4fdbe7e12829ab64caedc34c32ad1a6d742"
    end

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.0/seqviz-rs-x86_64-apple-darwin.tar.gz"
      sha256 "e5708252eaf1f33cac239dc4ae2d7853441aaada7976e710882aeae94ab18a09"
    end
  end

  on_linux do
    depends_on arch: :x86_64

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.0/seqviz-rs-x86_64-unknown-linux-musl.tar.gz"
      sha256 "204b08765c83b35b3330ffa40fe19b8043940975177cd95a853984a55e7d224a"
    end
  end

  conflicts_with "sq", because: "both install an sq executable"

  def install
    bin.install "sq"
    pkgshare.install "config", "contrib"
  end

  test do
    ENV["XDG_CACHE_HOME"] = (testpath/"cache").to_s
    (testpath/"example.fa").write ">record1 example\nACGT\nTGCA\n>record2\nNNNN\n"
    assert_equal ">record1 example\nACGTTGCA\n>record2\nNNNN\n",
                 shell_output("#{bin}/sq #{testpath}/example.fa")
    assert_equal "sq #{version}\n", shell_output("#{bin}/sq --version")
  end
end
