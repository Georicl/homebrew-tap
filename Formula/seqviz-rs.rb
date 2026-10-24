class SeqvizRs < Formula
  desc "Terminal browser for biological sequences and alignment records"
  homepage "https://github.com/Georicl/seqviz-rs"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.1/seqviz-rs-aarch64-apple-darwin.tar.gz"
      sha256 "14631ff1604b5199c5f44f1cd172d236061c9f231e287e47c4148c8ad55c40fa"
    end

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.1/seqviz-rs-x86_64-apple-darwin.tar.gz"
      sha256 "4b5a1935842433b9edc7e1a18aa689de9d5cb8d9fd608e519730a92ae39b04ef"
    end
  end

  on_linux do
    depends_on arch: :x86_64

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.1/seqviz-rs-x86_64-unknown-linux-musl.tar.gz"
      sha256 "da199fddca9adaf4523e4b51a9527311c3b84436a6e3769798b74be258484894"
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
