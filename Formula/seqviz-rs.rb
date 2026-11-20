class SeqvizRs < Formula
  desc "Terminal browser for biological sequences and alignment records"
  homepage "https://github.com/Georicl/seqviz-rs"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v2.2.1/seqviz-rs-aarch64-apple-darwin.tar.gz"
      sha256 "d87db80d9664b5a0a7393831816a9971fdb4ca410298607fbb7f35fb1f351a72"
    end

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v2.2.1/seqviz-rs-x86_64-apple-darwin.tar.gz"
      sha256 "ab74dd7e7df15d76d8a2893123684c19d1ae323388872e0d98edd339c73b409e"
    end
  end

  on_linux do
    depends_on arch: :x86_64

    on_intel do
      url "https://github.com/Georicl/seqviz-rs/releases/download/v2.2.1/seqviz-rs-x86_64-unknown-linux-musl.tar.gz"
      sha256 "77a93964b1e76cf5052c2fe550b10ec5118e5696d10a084b6d80864da0e1c6c7"
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
    assert_equal "seqviz #{version}\n", shell_output("#{bin}/sq --version")
  end
end
