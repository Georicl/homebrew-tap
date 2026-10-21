class SeqvizRs < Formula
  desc "Terminal browser for biological sequences and alignment records"
  homepage "https://github.com/Georicl/seqviz-rs"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.1.0/seqviz-rs-aarch64-apple-darwin.tar.gz"
      sha256 "30c19120de6c474176ef57fca9e4cb481c7f892a81faa899b38a1d604f6b086b"
    end

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.1.0/seqviz-rs-x86_64-apple-darwin.tar.gz"
      sha256 "d97ff22882f8d56457e6ae8e5573723692d493a9a0cf03a531a8833985271d9d"
    end
  end

  on_linux do
    depends_on arch: :x86_64

    url "https://github.com/Georicl/seqviz-rs/releases/download/v0.1.0/seqviz-rs-x86_64-unknown-linux-musl.tar.gz"
    sha256 "d2b3b1f85d24139bb2b7f910c7eafe52225effc4aa548d2d48d8aa6c308a7466"
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
