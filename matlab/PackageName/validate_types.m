function result = validate_types(data, column, expected_type)
    % validate_types - Validate that all values match expected type.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or empty (for numeric data).
    %   expected_type: Type string ('numeric', 'integer', 'double').
    %
    % Returns:
    %   true if all non-NaN values match the expected type.

    if isempty(data)
        result = true;
        return;
    end

    if isstruct(data)
        values = [data.(column)];
    else
        values = data(:)';
    end

    values = values(~isnan(values));

    switch expected_type
        case 'numeric'
            result = all(isnumeric(values));
        case 'integer'
            result = all(isnumeric(values) & (values == floor(values)));
        case 'double'
            result = all(isa(values, 'double'));
        otherwise
            error('Unknown type: %s', expected_type);
    end
end
