class ChainCommit:

    ECID = 0x02
    BITLENGTH = 200

    def __init__(self, timestamp: bytes, chain_id_hash: bytes, commit_weld: bytes, entry_hash: bytes,
                 ec_spent: int, ec_public_key: bytes, signature: bytes, **kwargs):
        # Required fields. Must be in every ChainCommit
        self.timestamp = timestamp
        self.chain_id_hash = chain_id_hash
        self.commit_weld = commit_weld
        self.entry_hash = entry_hash
        self.ec_spent = ec_spent
        self.ec_public_key = ec_public_key
        self.signature = signature
        # TODO: assert they're all here
        # TODO: use kwargs for some optional metadata

    def marshal(self):
        """Marshals the ChainCommit according to the byte-level representation shown at
        https://github.com/FactomProject/FactomDocs/blob/master/factomDataStructureDetails.md#chain-commit
        """
        buf = bytearray()
        buf.append(0x00)
        buf.extend(self.timestamp)
        buf.extend(self.chain_id_hash)
        buf.extend(self.commit_weld)
        buf.extend(self.entry_hash)
        buf.append(self.ec_spent)
        buf.extend(self.ec_public_key)
        buf.extend(self.signature)
        return bytes(buf)

    @classmethod
    def unmarshal(cls, raw: bytes):
        """Returns a new ChainCommit object, unmarshalling given bytes according to:
        https://github.com/FactomProject/FactomDocs/blob/master/factomDataStructureDetails.md#chain-commit
        """
        data = raw[1:]  # skip single byte version, probably just 0x00 anyways
        timestamp, data = data[:6], data[6:]
        chain_id_hash, data = data[:32], data[32:]
        commit_weld, data = data[:32], data[32:]
        entry_hash, data = data[:32], data[32:]
        ec_spent, data = data[:1], data[1:]
        ec_spent = int.from_bytes(ec_spent, byteorder='big')
        assert 10 < ec_spent < 21, 'Invalid EC spent!'  # 10 EC for creation + 1 EC per KB up to 10 KB
        ec_public_key, data = data[:32], data[32:]
        signature, data = data[:64], data[64:]  # covers version through ec spent
        assert len(data) == 0, 'Extra bytes remaining!'

        return ChainCommit(
            timestamp=timestamp,
            chain_id_hash=chain_id_hash,
            commit_weld=commit_weld,
            entry_hash=entry_hash,
            ec_spent=ec_spent,
            ec_public_key=ec_public_key,
            signature=signature
        )

    def to_dict(self):
        pass  # TODO: Implement ChainCommit.to_dict()

    def __str__(self):
        # TODO: convert timestamp to readable and EC Public Key to its base58 address
        return '{}(timestamp={}, entry_hash={}, ec_public_key={})'.format(
            self.__class__.__name__, self.timestamp, self.entry_hash.hex(), self.ec_public_key.hex())
