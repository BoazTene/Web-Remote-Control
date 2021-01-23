pub fn encrypt(string: &str) -> md5::Digest{
    md5::compute(string.as_bytes())
}