class SeqvizRs < Formula
  desc "Terminal browser for biological sequences and alignment records"
  homepage "https://github.com/Georicl/seqviz-rs"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.2/seqviz-rs-aarch64-apple-darwin.tar.gz"
      sha256 "4627ff3c41908d920dfe5b6169a7952b063a10ed73943f4256ce902fa2d3ad19"
    end

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.2/seqviz-rs-x86_64-apple-darwin.tar.gz"
      sha256 "c5d1a56f676a9a9577de778371e4646d6fc11a90ceeee97743e8ddfd3af04aa4"
    end
  end

  on_linux do
    depends_on arch: :x86_64

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v0.2.2/seqviz-rs-x86_64-unknown-linux-musl.tar.gz"
      sha256 "8d114ee2843b8ed3dc3efdbc4258beed4a16774c62443ef1b36b953fcd96cd2e"
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
